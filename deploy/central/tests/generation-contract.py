"""Exercise generation upgrade against an in-memory API, never a cluster."""
import copy,importlib.util,json,sys,tempfile
from pathlib import Path
from unittest.mock import patch
root=Path(__file__).resolve().parents[1]
def load(name,file):
 s=importlib.util.spec_from_file_location(name,root/'deployment'/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
r=load('grender','render.py');u=load('gupgrade','generation-upgrade.py');m=load('ginstall','install.py')
with tempfile.TemporaryDirectory() as tmp:
 state=Path(tmp);state.chmod(0o700)
 b={'context':'rit-byrokratt','applicationNamespace':r.OWNER,'expectedAPIServer':'https://test.invalid','expectedKubeSystemUID':'system','expectedCentralNamespaceUID':'central','expectedVaultClusterID':'vault','frontendAccessMode':'port-forward','frontendOrigin':'http://localhost:18080','storageClass':'fixture','vaultAddress':'https://vault.test','workloadVaultAddress':'https://vault.central.svc','vaultPodSelector':{'app':'vault'},'vaultKVMount':'secret','vaultAppRoleMount':'approle','kubernetesAPICIDR':'10.96.0.1/32'}
 images={k:'test.invalid/'+k+'@sha256:'+'1'*64 for k in r.IMAGE_KEYS};old,stages,_=r.render(b,images,state)
 # Reconstruct the previous package's two missing embedding envs/service port.
 for o in old['items']:
  if o['kind']=='Service' and o['metadata']['name']==r.OWNER+'-backend':o['spec']['ports']=[p for p in o['spec']['ports'] if p['name']!='resql']
  if o['kind']=='Deployment' and o['metadata']['name']==r.OWNER+'-llm':
   for co in o['spec']['template']['spec']['containers']:
    co['env']=[e for e in co['env'] if e['name'] not in ['GUARDRAILS_EMBEDDING_PATH','FASTEMBED_CACHE_PATH']]
 (state/'installation.json').write_text(json.dumps(old));(state/'stages.json').write_text(json.dumps(stages));(state/'protected-baseline.json').write_text('{}')
 binding=state/'bindings.json';binding.write_text(json.dumps(b));imagefile=state/'images.json';imagefile.write_text(json.dumps(images))
 image='ghcr.io/buerokratt/llm-module/central-llm@sha256:'+'2'*64;cidr='8.8.8.8/32'
 _,_,desired,_,_,targets=u.prepare(b,images,state,image,[cidr])
 identity=lambda o:(o['kind'],o['metadata']['name'])
 live={identity(o):copy.deepcopy(o) for o in old['items']}
 # Accept exactly the temporary generation flag and service-port repairs in report.
 for obj in live.values():
  if obj['kind']=='Service' and obj['metadata']['name']==r.OWNER+'-backend':obj['spec']['ports'].append({'name':'resql','port':8082,'targetPort':8082})
  if obj['kind']=='Deployment' and obj['metadata']['name'] in [r.OWNER+'-llm',r.OWNER+'-notification']:
   for co in obj['spec']['template']['spec']['containers']:
    for e in co['env']:
     if e['name']=='LLM_GENERATION_ENABLED':e['value']='true'
 policy=next(copy.deepcopy(o) for o in targets if o['kind']=='NetworkPolicy');policy['metadata']['labels']={m.LABEL:m.OWNER};policy['metadata']['annotations']={'buerokratt.ee/purpose':'Generation acceptance fixture'};live[identity(policy)]=policy
 for o in live.values():o['metadata']['resourceVersion']='1'
 calls=[]
 class FakeInstaller(m.Installer):
  def __init__(self,*args):self.state=state
  def identity(self):pass
  def preservation(self,first=False):pass
  def wait(self,o):assert o['kind'] in ['Deployment','Service','NetworkPolicy','ConfigMap']
  def kube(self,ns,*args,payload=None,**kw):
   assert ns==r.OWNER
   if args[0]=='get':return copy.deepcopy(live.get((args[1],args[2])))
   dry='--dry-run=server' in args
   if args[0]=='create':out=copy.deepcopy(payload)
   else:
    out=copy.deepcopy(live[(args[1],args[2])])
    for operation in json.loads(args[args.index('-p')+1]):
     keys=operation['path'].strip('/').split('/');parent=out
     for key in keys[:-1]:parent=parent[key]
     if operation['op']=='test':assert parent[keys[-1]]==operation['value']
     else:parent[keys[-1]]=operation['value']
   out['metadata'].setdefault('resourceVersion','1')
   if not dry:calls.append(identity(out));live[identity(out)]=out
   return out
 fake=type('Module',(),{'Installer':FakeInstaller,'OWNER':m.OWNER,'LABEL':m.LABEL,'HASH':m.HASH})
 real_load=u.load
 def modules(name,file):return fake if file=='install.py' else real_load(name,file)
 argv=['upgrade','--bindings',str(binding),'--images',str(imagefile),'--kubeconfig','fixture','--state-dir',str(state),'--llm-image',image,'--provider-cidr',cidr]
 before={p.name:p.read_bytes() for p in state.iterdir() if p.is_file()}
 with patch.object(u,'load',modules),patch.object(sys,'argv',argv):u.main()
 assert not calls and before=={p.name:p.read_bytes() for p in state.iterdir() if p.is_file()}
 with patch.object(u,'load',modules),patch.object(sys,'argv',argv+['--execute']):u.main()
 assert len(calls)==4 and (state/'before-runtime-upgrade-222222222222/installation.json').read_bytes()==before['installation.json']
 calls.clear()
 argv+=['--enable-general-knowledge','--frontend-image','ghcr.io/buerokratt/noops/central-frontend@sha256:'+'3'*64,'--widget-datamapper','ghcr.io/buerokratt/datamapper/central-datamapper@sha256:'+'4'*64,'--enable-widget-llm']
 with patch.object(u,'load',modules),patch.object(sys,'argv',argv+['--execute']):u.main()
 assert len(calls)==8 and (state/'before-runtime-upgrade-222222222222/installation.json').read_bytes()==before['installation.json']
 assert json.loads(binding.read_text())['llmGenerationEnabled'] is True
 with patch.object(u,'load',modules),patch.object(sys,'argv',argv+['--execute']):u.main()
 live[('Deployment',r.OWNER+'-llm')]['spec']['template']['spec']['containers'][0]['image']='foreign:drift'
 with patch.object(u,'load',modules),patch.object(sys,'argv',argv):
  try:u.main()
  except ValueError as exc:assert 'unexpected_live_contract' in str(exc)
  else:raise AssertionError('foreign drift accepted')
 health=load('generation_health','health.py')
 assert 'disabled' in health.llm_health_check({}, {'generation_enabled':False,'redis_session_store':'connected'})
 assert 'enabled' in health.llm_health_check({'llmGenerationEnabled':True},{'generation_enabled':True,'redis_session_store':'connected','guardrails_embedding_loaded':True})
 for bad in [{'generation_enabled':True,'redis_session_store':'connected'},{'generation_enabled':False,'redis_session_store':'connected','guardrails_embedding_loaded':True},{'generation_enabled':True,'redis_session_store':'disconnected','guardrails_embedding_loaded':True}]:
  try:health.llm_health_check({'llmGenerationEnabled':True},bad)
  except health.Stop:pass
  else:raise AssertionError('unhealthy generating service accepted')
 print(json.dumps({'status':'PASS','planReadOnly':True,'eightScopedTargetsOnly':True,'existingStateBackupExact':True,'temporaryOperatorChangesAccepted':True,'retryPass':True,'foreignDriftRejected':True,'clusterCalls':0}))
