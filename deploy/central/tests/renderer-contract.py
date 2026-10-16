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
 print(json.dumps({'status':'PASS','resources':len(seen),'repeatRenderExact':True,'nonrootAndDigestBindings':True,'storageKeysSchemaNotRuntimeInitializers':True,'scopeAndUnboundNegatives':4}))
