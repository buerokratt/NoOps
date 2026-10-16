import importlib.util,json,subprocess,tempfile,hashlib,base64
from pathlib import Path
root=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('renderer',root/'deployment/render.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
with tempfile.TemporaryDirectory(prefix='fresh-render-',dir='/tmp') as td:
 state=Path(td);state.chmod(0o700);cert=state/'frontend.crt';key=state/'frontend.key'
 subprocess.run(['openssl','req','-x509','-newkey','rsa:2048','-nodes','-days','1','-subj','/CN=fresh-render.test','-addext','subjectAltName=DNS:fresh-render.test','-keyout',str(key),'-out',str(cert)],check=True,capture_output=True);key.chmod(0o600)
 b={'context':'rit-byrokratt','applicationNamespace':'central-byk-test','expectedAPIServer':'https://test.invalid','expectedKubeSystemUID':'test-system-uid','expectedCentralNamespaceUID':'test-central-uid','expectedVaultClusterID':'test-vault-id','frontendOrigin':'https://fresh-render.test','storageClass':'test-storage','ingressClass':'nginx','vaultAddress':'https://test-vault.test','workloadVaultAddress':'https://vault.central.svc','vaultPodSelector':{'app':'vault'},'ingressNamespace':'ingress-nginx','vaultKVMount':'secret','vaultAppRoleMount':'approle','kubernetesAPICIDR':'10.96.0.1/32','frontendTLSCertFile':str(cert),'frontendTLSKeyFile':str(key)}
 images={k:'test.invalid/byk/'+k+'@sha256:'+hashlib.sha256(k.encode()).hexdigest() for k in r.IMAGE_KEYS}
 manifest,stages,c=r.render(b,images,state);second,_,c2=r.render(b,images,state);assert manifest==second and c==c2
 seen=set()
 for obj in manifest['items']:
  m=obj['metadata'];identity=(obj['kind'],m.get('namespace'),m['name']);assert identity not in seen;seen.add(identity)
  assert m.get('namespace','central-byk-test') in ['central-byk-test','central'];assert m['labels']['buerokratt.ee/deployment']=='central-byk-test'
  cp=json.loads(json.dumps(obj));h=cp['metadata']['annotations'].pop('buerokratt.ee/creation-sha256');assert hashlib.sha256(json.dumps(cp,sort_keys=True).encode()).hexdigest()==h
  if obj['kind'] in ['Deployment','StatefulSet','Job']:
   pod=obj['spec']['template']['spec'];assert pod['securityContext']['runAsNonRoot'];assert not pod.get('hostNetwork');assert not pod.get('hostPID')
   names={v['name'] for v in pod.get('volumes',[])};assert len(names)==len(pod.get('volumes',[]))
   for co in pod['containers']+pod.get('initContainers',[]):
    assert '@sha256:' in co['image'];assert co['securityContext']['allowPrivilegeEscalation']==False
    assert all(m['name'] in names for m in co.get('volumeMounts',[]))
   if obj['kind']!='Job':assert not any('initialize' in co['name'] or 'liquibase' in co['name'] for co in pod.get('initContainers',[]))
 # API egress must use an exact bound destination tuple and only delivery Pods.
 def api_policy(value):
  return next(o for o in value['items'] if o['kind']=='NetworkPolicy' and o['metadata']['name']=='vault-delivery-api')
 legacy=api_policy(manifest)
 assert legacy['spec']['egress']==[{'to':[{'ipBlock':{'cidr':'10.96.0.1/32'}}],'ports':[{'protocol':'TCP','port':443}]}]
 endpoint={**b,'kubernetesAPICIDR':'192.0.2.119/32','kubernetesAPIPort':6443}
 routed,_,_=r.render(endpoint,images,state);policy=api_policy(routed)
 assert policy['spec']['egress']==[{'to':[{'ipBlock':{'cidr':'192.0.2.119/32'}}],'ports':[{'protocol':'TCP','port':6443}]}]
 assert policy['metadata']['namespace']=='central-byk-test'
 assert policy['spec']['podSelector']==legacy['spec']['podSelector']
 values=policy['spec']['podSelector']['matchExpressions']
 assert values==[{'key':'app','operator':'In','values':['vault-deliver-'+x for x in c['accounts']]}]
 def except_api(value):
  return [o for o in value['items'] if not (o['kind']=='NetworkPolicy' and o['metadata']['name']=='vault-delivery-api')]
 assert except_api(routed)==except_api(manifest)
 explicit,_,_=r.render({**b,'kubernetesAPIPort':443},images,state)
 assert explicit==manifest
 for invalid in [None,True,False,0,-1,65536,'6443',6443.0]:
  try:r.render({**endpoint,'kubernetesAPIPort':invalid},images,state)
  except r.Stop as exc:assert str(exc)=='invalid_kubernetes_api_port'
  else:raise AssertionError('invalid API port accepted')
 # Port-forward mode needs no frontend DNS/TLS or ingress controller.
 local={**endpoint,'frontendAccessMode':'port-forward','frontendOrigin':'http://localhost:18080','frontendTLSCertFile':None,'frontendTLSKeyFile':None,'ingressClass':None,'ingressNamespace':None}
 forwarded,pstages,_=r.render(local,images,state)
 assert len(forwarded['items'])==98 and pstages['ingress']==[]
 assert not any(o['kind']=='Ingress' or o['kind']=='Secret' and o['metadata']['name']=='frontend-tls' for o in forwarded['items'])
 net=next(o for o in forwarded['items'] if o['kind']=='NetworkPolicy' and o['metadata']['name']=='test-isolation')
 assert net['spec']['ingress']==[{'from':[{'podSelector':{}}]}]
 assert api_policy(forwarded)['spec']['egress']==policy['spec']['egress']
 backend_local=next(o for o in forwarded['items'] if o['kind']=='Deployment' and o['metadata']['name']=='central-byk-test-backend')['spec']['template']['spec']
 assert [co['name'] for co in backend_local['containers']]==['ruuter-public','ruuter-private','resql','tim','mapper','cron','adapter-chatbot','adapter-common','adapter-service','adapter-logging','service-pipeline','vault-agent-cron']
 for co in backend_local['containers']:
  if co['name'].startswith('ruuter-'):
   assert next(e['value'] for e in co['env'] if e['name']=='application.cors.allowedOrigins')=='http://localhost:18080'
 for invalid_origin in ['http://example.invalid:18080','https://example.invalid','http://localhost.evil.invalid:18080','http://user@localhost:18080','http://localhost:18080/path','http://localhost:18080?x=1','http://localhost:18080#fragment']:
  try:r.render({**local,'frontendOrigin':invalid_origin},images,state)
  except r.Stop:pass
  else:raise AssertionError('non-loopback or malformed origin accepted')
 for mode in [None,'invalid']:
  try:r.render({**local,'frontendAccessMode':mode},images,state)
  except r.Stop:pass
  else:raise AssertionError('invalid access mode accepted')
 # Generation is explicit and permits only bound public provider host IPs.
 enabled,_,_=r.render({**local,'llmGenerationEnabled':True,'llmProviderCIDRs':['8.8.8.8/32']},images,state)
 provider=next(o for o in enabled['items'] if o['kind']=='NetworkPolicy' and o['metadata']['name']=='llm-provider-egress')
 assert provider['spec']['podSelector']=={'matchLabels':{'app':'central-byk-test-llm'}}
 assert provider['spec']['egress']==[{'to':[{'ipBlock':{'cidr':'8.8.8.8/32'}}],'ports':[{'protocol':'TCP','port':443}]}]
 for name in ['llm','notification']:
  pod=next(o for o in enabled['items'] if o['kind']=='Deployment' and o['metadata']['name']=='central-byk-test-'+name)['spec']['template']['spec']
  co=next(c for c in pod['containers'] if c['name']==name)
  assert next(e['value'] for e in co['env'] if e['name']=='LLM_GENERATION_ENABLED')=='true'
 backend_service=next(o for o in enabled['items'] if o['kind']=='Service' and o['metadata']['name']=='central-byk-test-backend')
 assert {'name':'resql','port':8082,'targetPort':8082} in backend_service['spec']['ports']
 for bad in [{'llmGenerationEnabled':'true'},{'llmGenerationEnabled':True},{'llmProviderCIDRs':['0.0.0.0/0']},{'llmProviderCIDRs':['10.0.0.1/32']},{'llmProviderCIDRs':['8.8.8.0/24']},{'llmProviderCIDRs':'8.8.8.8/32'}]:
  try:r.render({**local,**bad},images,state)
  except r.Stop:pass
  else:raise AssertionError('unsafe generation binding accepted')
 assert list(stages)==['namespace','storage','provision','schema','vaultDelivery','engineBootstrap','applications','ingress']
 backend=next(o for o in manifest['items'] if o['kind']=='Deployment' and o['metadata']['name']=='central-byk-test-backend')['spec']['template']['spec']
 for co in backend['containers']:
  if co['name'].startswith('ruuter-'):
   assert next(e['value'] for e in co['env'] if e['name']=='application.cors.allowedOrigins')==b['frontendOrigin']
 private=next(co for co in backend['containers'] if co['name']=='ruuter-private')
 assert any(v['name']=='service-empty-state' and v['mountPath']=='/DSL/services/GET/slots.yml' and v['readOnly'] for v in private['volumeMounts'])
 for change in [{'context':'rit-byrokratt-stage'},{'applicationNamespace':'cl13-llm'},{'expectedVaultClusterID':None},{'frontendOrigin':'http://fresh-render.test'}]:
  try:r.render({**b,**change},images,state)
  except r.Stop:pass
  else:raise AssertionError('unsafe binding accepted')
 sql=next(o for o in manifest['items'] if o['kind']=='Secret' and o['metadata']['name']=='database-provision')['data']['provision.sql'];assert '\n\\gexec' in base64.b64decode(sql).decode()
 print(json.dumps({'status':'PASS','resources':len(seen),'repeatRenderExact':True,'nonrootAndDigestBindings':True,'storageKeysSchemaNotRuntimeInitializers':True,'scopeAndUnboundNegatives':4,'apiEgressEndpoint6443':True,'legacy443Compatible':True,'apiPortNegatives':8,'otherResourcesUnchanged':True,'portForwardResources':98,'noFrontendTLSOrIngress':True,'portForwardOriginNegatives':7}))
