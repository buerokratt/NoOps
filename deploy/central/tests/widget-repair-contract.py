"""Known-bad override repair, read-only planning, retry and drift rejection."""
import copy,hashlib,importlib.util,json,sys,tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
root=Path(__file__).resolve().parents[1]
def load(name,file):
 s=importlib.util.spec_from_file_location(name,root/'deployment'/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
u=load('repair','repair-widget-yaml.py');m=load('repair_install','install.py')
def hash_cm(cm):
 cm['metadata']['annotations'].pop(m.HASH,None);cm['metadata']['annotations'][m.HASH]=hashlib.sha256(json.dumps(cm,sort_keys=True).encode()).hexdigest()
with tempfile.TemporaryDirectory() as td:
 state=Path(td);state.chmod(0o700);binding=state/'bindings.json';binding.write_text('{}')
 cm={'apiVersion':'v1','kind':'ConfigMap','metadata':{'name':'widget-runtime-fixes','namespace':m.OWNER,'labels':{m.LABEL:m.OWNER},'annotations':{}},'data':{'private-2':u.BAD+'\n','other':'preserve'}};hash_cm(cm)
 dep={'apiVersion':'apps/v1','kind':'Deployment','metadata':{'name':m.OWNER+'-backend','labels':{m.LABEL:m.OWNER},'annotations':{m.HASH:'backend-original'}},'spec':{'template':{'metadata':{'labels':{'app':'backend'}},'spec':{'containers':[{'name':'ruuter-private','image':'fixture@sha256:'+'1'*64,'volumeMounts':[]}],'volumes':[]}}}}
 original={'apiVersion':'v1','kind':'List','items':[cm,dep,{'kind':'Job','metadata':{'name':'schema-preserved'}}]};saved=state/'installation.json';saved.write_text(json.dumps(original));before=saved.read_bytes()
 live={('ConfigMap','widget-runtime-fixes'):copy.deepcopy(cm),('Deployment',m.OWNER+'-backend'):copy.deepcopy(dep)}
 for o in live.values():o['metadata']['resourceVersion']='1'
 calls=[]
 class Fake(m.Installer):
  def __init__(self,*a):pass
  def identity(self):pass
  def preservation(self,*a,**kw):pass
  def wait(self,o):assert o['kind']=='Deployment'
  def kube(self,ns,*args,**kw):
   assert ns==m.OWNER
   if args[0]=='get':return copy.deepcopy(live[(args[1],args[2])])
   assert args[0]=='patch';key=(args[1],args[2]);o=copy.deepcopy(live[key]);ops=json.loads(args[args.index('-p')+1])
   for op in ops:
    names=op['path'].strip('/').split('/');parent=o
    for n in names[:-1]:parent=parent[n]
    if op['op']=='test':assert parent[names[-1]]==op['value']
    else:parent[names[-1]]=op['value']
   if '--dry-run=server' not in args:
    calls.append(key);o['metadata']['resourceVersion']=str(int(o['metadata']['resourceVersion'])+1);live[key]=o
   return o
 fake=SimpleNamespace(Installer=Fake,OWNER=m.OWNER,LABEL=m.LABEL,HASH=m.HASH)
 argv=['repair','--package',str(root),'--bindings',str(binding),'--kubeconfig','fixture','--state-dir',str(state)]
 with patch.object(u,'load',lambda package:fake),patch.object(sys,'argv',argv):u.main()
 assert not calls and saved.read_bytes()==before
 with patch.object(u,'load',lambda package:fake),patch.object(sys,'argv',argv+['--execute']):u.main()
 wanted=json.loads(saved.read_text());assert wanted['items'][1:]==original['items'][1:]
 assert (state/'before-widget-yaml-repair/installation.json').read_bytes()==before
 assert live[('ConfigMap','widget-runtime-fixes')]['data']['private-2']==u.GOOD+'\n'
 assert live[('ConfigMap','widget-runtime-fixes')]['data']['other']=='preserve'
 template=copy.deepcopy(live[('Deployment',m.OWNER+'-backend')]['spec']['template'])
 with patch.object(u,'load',lambda package:fake),patch.object(sys,'argv',argv+['--execute']):u.main()
 assert live[('Deployment',m.OWNER+'-backend')]['spec']['template']==template
 assert set(calls)=={('ConfigMap','widget-runtime-fixes'),('Deployment',m.OWNER+'-backend')}
 live[('ConfigMap','widget-runtime-fixes')]['data']['other']='foreign'
 with patch.object(u,'load',lambda package:fake),patch.object(sys,'argv',argv):
  try:u.main()
  except ValueError as exc:assert 'unrelated_config_drift' in str(exc)
  else:raise AssertionError('foreign drift accepted')
 print(json.dumps({'status':'PASS','twoScopedTargetsOnly':True,'planReadOnly':True,'backupExact':True,'retryNoExtraRollout':True,'foreignDriftRejected':True,'clusterCalls':0}))
