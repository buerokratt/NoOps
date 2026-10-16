#!/usr/bin/env python3
"""Operator-only, identity-bound fresh installer. Never applies historical migrations."""
import argparse,hashlib,json,os,subprocess,sys,time
from pathlib import Path
OWNER='central-byk-test';LABEL='buerokratt.ee/deployment';HASH='buerokratt.ee/creation-sha256'
class Stop(Exception):pass
class Installer:
 def __init__(self,binding,kubeconfig,state):
  self.b=binding;self.state=state
  if binding.get('context')!='rit-byrokratt' or binding.get('applicationNamespace')!=OWNER:raise Stop('target_scope_mismatch')
  mode=binding.get('frontendAccessMode','ingress')
  if mode not in ('ingress','port-forward'):raise Stop('invalid_frontend_access_mode')
  if mode=='port-forward':
   u=__import__('urllib.parse',fromlist=['urlsplit']).urlsplit(binding.get('frontendOrigin') or '')
   if u.scheme not in ('http','https') or u.hostname not in ('localhost','127.0.0.1','::1') or u.username or u.password or u.path not in ('','/') or u.query or u.fragment:raise Stop('port_forward_requires_loopback_origin')
  self.base=['kubectl','--kubeconfig',str(Path(kubeconfig).resolve(strict=True)),'--context','rit-byrokratt','--request-timeout=30s']
 def kube(self,ns,*args,payload=None,missing=False,timeout=90):
  command=self.base+['--namespace',ns]+list(args)+(['--ignore-not-found'] if missing else [])
  try:r=subprocess.run(command,input=None if payload is None else json.dumps(payload).encode(),capture_output=True,timeout=timeout)
  except subprocess.TimeoutExpired:raise Stop('kubernetes_timeout') from None
  if r.returncode:raise Stop('kubernetes_'+args[0]+'_failed')
  try:return json.loads(r.stdout) if r.stdout.strip() else None
  except ValueError:return None
 def identity(self):
  v=self.kube(OWNER,'config','view','--minify','-o','json')
  if len(v.get('clusters',[]))!=1 or v['clusters'][0]['cluster']['server']!=self.b.get('expectedAPIServer'):raise Stop('api_server_mismatch')
  for name,field in [('kube-system','expectedKubeSystemUID'),('central','expectedCentralNamespaceUID')]:
   if self.kube(OWNER,'get','namespace',name,'-o','json')['metadata']['uid']!=self.b.get(field):raise Stop('namespace_identity_mismatch_'+name)
  sc=self.kube(OWNER,'get','storageclass',self.b['storageClass'],'-o','json')
  if sc.get('provisioner')=='kubernetes.io/no-provisioner' and not self.b.get('preboundStorageVerified'):raise Stop('static_storage_requires_prebound_contract')
  if self.b.get('frontendAccessMode','ingress')=='port-forward':return
  self.kube(OWNER,'get','ingressclass',self.b['ingressClass'],'-o','json')
  host=__import__('urllib.parse',fromlist=['urlsplit']).urlsplit(self.b['frontendOrigin']).hostname
  routes=self.kube(OWNER,'get','ingresses','--all-namespaces','-o','json')['items']
  for route in routes:
   if any(rule.get('host')==host for rule in route.get('spec',{}).get('rules',[])) and not (route['metadata'].get('namespace')==OWNER and route['metadata'].get('labels',{}).get(LABEL)==OWNER):raise Stop('frontend_host_already_bound')
 def protected(self):
  result={}
  for ns in ['cl13-llm','central']:
   data=self.kube(ns,'get','pods,pvc,pv,deployments,statefulsets,services,configmaps','-o','json')
   retained=[]
   for x in data['items']:
    if x['metadata'].get('labels',{}).get(LABEL)==OWNER:continue
    if x['kind']=='PersistentVolume':
     claim=x.get('spec',{}).get('claimRef',{})
     if claim.get('namespace')==OWNER:continue
     if claim.get('namespace')=='central' and claim.get('name')=='opensearch-data':
      pvc=self.kube('central','get','pvc','opensearch-data','-o','json',missing=True)
      if pvc and pvc['metadata'].get('labels',{}).get(LABEL)==OWNER and pvc['metadata']['uid']==claim.get('uid'):continue
    if x['kind']=='PersistentVolume' and x.get('spec',{}).get('claimRef',{}).get('namespace') not in ['central','cl13-llm']:continue
    m=x['metadata'];entry={'kind':x['kind'],'name':m['name'],'uid':m['uid'],'spec':x.get('spec'),'dataHash':hashlib.sha256(json.dumps(x.get('data'),sort_keys=True).encode()).hexdigest()}
    if x['kind']=='Pod':entry['containers']=[{k:s.get(k) for k in ['name','containerID','restartCount']} for s in x.get('status',{}).get('containerStatuses',[])+x.get('status',{}).get('initContainerStatuses',[])]
    retained.append(entry)
   result[ns]=sorted(retained,key=lambda x:(x['kind'],x['name']))
  return result
 def preservation(self,first=False):
  p=self.state/'protected-baseline.json';now=self.protected()
  if not p.exists():
   if not first:raise Stop('preservation_baseline_missing')
   p.write_text(json.dumps(now,sort_keys=True));p.chmod(0o600)
  elif json.loads(p.read_text())!=now:raise Stop('protected_runtime_or_storage_changed')
 def contract(self,obj):
  if obj['kind']=='ConfigMap':return {key:obj.get(key,{}) for key in ['data','binaryData']}
  if obj['kind'] in ['Deployment','StatefulSet']:pod=obj['spec']['template']['spec']
  elif obj['kind']=='Job':pod=obj['spec']['template']['spec']
  else:return None
  import copy
  pod=copy.deepcopy(pod)
  for v in pod.get('volumes',[]):
   for typ in ['secret','configMap']:
    if typ in v:v[typ].setdefault('defaultMode',420)
  def clean(x):
   if isinstance(x,dict):
    values={k:clean(v) for k,v in x.items()}
    return {k:v for k,v in values.items() if v is not None and v is not False and v!=[] and v!={}}
   if isinstance(x,list):return [clean(v) for v in x]
   return x
  return clean({'containers':[{k:c.get(k) for k in ['name','image','command','args','env','volumeMounts','securityContext','workingDir']} for c in pod.get('containers',[])+pod.get('initContainers',[])],'volumes':pod.get('volumes',[]),'securityContext':pod.get('securityContext'),'serviceAccountName':pod.get('serviceAccountName'),'automountServiceAccountToken':pod.get('automountServiceAccountToken')})
 def create(self,obj,execute):
  kind=obj['kind'];m=obj['metadata'];ns=m.get('namespace',OWNER)
  if ns not in [OWNER,'central']:raise Stop('manifest_namespace_scope')
  if kind=='Namespace' and m['name']!=OWNER:raise Stop('namespace_scope')
  if ns=='central' and (m['name'] not in ['engine-tls','engine-ca','engine-admin','opensearch-data','engine-nginx','engine-isolation',OWNER+'-opensearch',OWNER+'-registry-pull']):raise Stop('shared_namespace_resource_scope')
  if m.get('labels',{}).get(LABEL)!=OWNER:raise Stop('unowned_manifest')
  old=self.kube(ns,'get',kind,m['name'],'-o','json',missing=True)
  if old:
   if old['metadata'].get('labels',{}).get(LABEL)!=OWNER or old['metadata'].get('annotations',{}).get(HASH)!=m['annotations'][HASH]:raise Stop('existing_resource_conflict_'+kind+'_'+m['name'])
   if kind=='Secret':
    expected=obj.get('data',{})
    if not expected and m['name'] in ['os-'+x for x in ['bootstrap','chatbot','common','service','knowledge','logging']]:
     import base64
     account=json.loads((self.state/'opensearch-accounts.json').read_text())['accounts'][m['name'][3:]]
     expected={key:base64.b64encode(value.encode()).decode() for key,value in {**account,'auth':account['username']+':'+account['password']}.items()}
    if old.get('data',{})!=expected or old.get('type','Opaque')!=obj.get('type','Opaque'):raise Stop('existing_secret_data_changed_'+m['name'])
   if self.contract(obj)!=self.contract(old):raise Stop('existing_workload_contract_changed_'+m['name'])
   return 'REUSED'
  admitted=self.kube(ns,'create','--dry-run=server','-f','-','-o','json',payload=obj)
  if kind=='Secret' and (admitted.get('data',{})!=obj.get('data',{}) or admitted.get('type','Opaque')!=obj.get('type','Opaque')):raise Stop('admission_secret_data_changed_'+m['name'])
  if self.contract(obj)!=self.contract(admitted):raise Stop('admission_workload_contract_changed_'+m['name'])
  if execute:self.kube(ns,'create','-f','-','-o','json',payload=obj)
  return 'CREATED' if execute else 'ADMITTED'
 def wait(self,obj):
  kind=obj['kind'];name=obj['metadata']['name'];ns=obj['metadata'].get('namespace',OWNER)
  if kind=='Job':
   deadline=time.monotonic()+600
   while time.monotonic()<deadline:
    status=self.kube(ns,'get','job',name,'-o','json').get('status',{})
    if status.get('succeeded',0)>=1:return
    if status.get('failed',0)>0 or any(c.get('type')=='Failed' and c.get('status')=='True' for c in status.get('conditions',[])):raise Stop('job_failed_'+name)
    time.sleep(2)
   raise Stop('job_timeout_'+name)
  elif kind in ['Deployment','StatefulSet']:self.kube(ns,'rollout','status',kind.lower()+'/'+name,'--timeout=600s',timeout=620)
 def run(self,manifest,stages,execute,token,kubeconfig):
  self.identity();self.preservation(first=True)
  objects={(x['kind'],x['metadata']['name'],x['metadata'].get('namespace')):x for x in manifest['items']}
  for stage,refs in stages.items():
   if stage=='vaultDelivery' and execute:
    args=[sys.executable,str(Path(__file__).with_name('operator-vault.py')),'--bindings',str(self.bpath),'--kubeconfig',kubeconfig,'--token-file',token,'--opensearch-credentials-file',str(self.state/'opensearch-accounts.json'),'--execute']
    result=subprocess.run(args,capture_output=True,timeout=180)
    if result.returncode:raise Stop('vault_provisioner_failed')
   for ref in refs:
    obj=objects[(ref['kind'],ref['name'],ref['namespace'])];action=self.create(obj,execute)
    print(json.dumps({'stage':stage,'kind':obj['kind'],'name':obj['metadata']['name'],'action':action}),flush=True)
    if execute:self.wait(obj)
   if execute:self.preservation()
  print(json.dumps({'status':'INSTALLED' if execute else 'ADMISSION_PASS','context':'rit-byrokratt','namespace':OWNER,'protectedResourcesExact':True}))
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--bindings',required=True);p.add_argument('--kubeconfig',required=True);p.add_argument('--state-dir',required=True);p.add_argument('--manifest',required=True);p.add_argument('--vault-token-file');p.add_argument('--execute',action='store_true');a=p.parse_args()
 state=Path(a.state_dir)
 if state.stat().st_mode&0o077:raise Stop('state_directory_must_be_private')
 if a.execute and not a.vault_token_file:raise Stop('private_vault_token_file_required')
 i=Installer(json.loads(Path(a.bindings).read_text()),a.kubeconfig,state);i.bpath=Path(a.bindings).resolve();i.run(json.loads(Path(a.manifest).read_text()),json.loads((state/'stages.json').read_text()),a.execute,a.vault_token_file,a.kubeconfig)
if __name__=='__main__':
 try:main()
 except Stop as e:print(json.dumps({'status':'STOPPED','reason':str(e)}));raise SystemExit(1)
