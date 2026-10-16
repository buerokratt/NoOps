import importlib.util,json,tempfile,copy,base64
from pathlib import Path
root=Path(__file__).resolve().parents[1];s=importlib.util.spec_from_file_location('installer',root/'deployment/install.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
with tempfile.TemporaryDirectory() as tmp:
 state=Path(tmp);k=state/'kube';k.write_text('not credential material')
 i=m.Installer({'context':'rit-byrokratt','applicationNamespace':'central-byk-test'},str(k),state)
 obj={'apiVersion':'apps/v1','kind':'Deployment','metadata':{'namespace':'central-byk-test','name':'owned-test','labels':{'buerokratt.ee/deployment':'central-byk-test'},'annotations':{'buerokratt.ee/creation-sha256':'fixture'}},'spec':{'template':{'spec':{'automountServiceAccountToken':False,'securityContext':{'runAsNonRoot':True},'containers':[{'name':'service','image':'fixture@sha256:'+'1'*64,'securityContext':{'allowPrivilegeEscalation':False},'volumeMounts':[]}], 'volumes':[]}}}}
 calls=[]
 def api(ns,*args,**kw):
  calls.append((ns,args))
  if args[0]=='get':return None
  return copy.deepcopy(kw['payload'])
 i.kube=api;assert i.create(obj,False)=='ADMITTED';assert not any('create'==a[0] and '--dry-run=server' not in a for _,a in calls)
 def injected(ns,*args,**kw):
  if args[0]=='get':return None
  result=copy.deepcopy(kw['payload']);result['spec']['template']['spec']['containers'][0]['image']='foreign:latest';return result
 i.kube=injected
 try:i.create(obj,True)
 except m.Stop as e:assert 'admission' in str(e)
 else:raise AssertionError('injected image accepted')
 def collision(ns,*args,**kw):
  result=copy.deepcopy(obj);result['metadata']['labels']={};return result
 i.kube=collision
 try:i.create(obj,True)
 except m.Stop as e:assert 'conflict' in str(e)
 else:raise AssertionError('unowned collision accepted')
 altered=copy.deepcopy(obj);altered['metadata']['namespace']='cl13-llm'
 try:i.create(altered,True)
 except m.Stop as e:assert 'namespace_scope' in str(e)
 else:raise AssertionError('protected namespace accepted')
 default=copy.deepcopy(obj);default['spec']['template']['spec']['containers'][0].pop('volumeMounts');default['spec']['template']['spec']['containers'][0]['securityContext']={};assert i.contract(obj)==i.contract(default)
 for kind in ['Secret','ConfigMap']:
  value={'apiVersion':'v1','kind':kind,'metadata':copy.deepcopy(obj['metadata']),'data':{'fixture':'c3ludGhldGlj'}}
  tampered=copy.deepcopy(value);tampered['data']['fixture']='Y2hhbmdlZA=='
  i.kube=lambda *args,**kw:tampered
  try:i.create(value,True)
  except m.Stop:pass
  else:raise AssertionError(kind+' data drift accepted with original hash annotation')
 account={'username':'synthetic-user','password':'synthetic-password'}
 (state/'opensearch-accounts.json').write_text(json.dumps({'accounts':{'bootstrap':account}}))
 delivered={'apiVersion':'v1','kind':'Secret','metadata':{**copy.deepcopy(obj['metadata']),'name':'os-bootstrap'},'data':{}}
 current=copy.deepcopy(delivered);current['data']={k:base64.b64encode(v.encode()).decode() for k,v in {**account,'auth':account['username']+':'+account['password']}.items()}
 i.kube=lambda *args,**kw:current
 assert i.create(delivered,False)=='REUSED'
 current['data']['auth']=base64.b64encode(b'wrong-auth').decode()
 try:i.create(delivered,False)
 except m.Stop:pass
 else:raise AssertionError('delivery auth drift accepted')
 print(json.dumps({'status':'PASS','readOnlyAdmission':True,'injectedImageRejected':True,'unownedCollisionRejected':True,'protectedNamespaceRejected':True,'harmlessAPIDefaultsNormalized':True,'secretAndConfigMapDataDriftRejected':True}))
