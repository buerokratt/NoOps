#!/usr/bin/env python3
"""Operator-only, scoped upgrade of an existing test installation; plan by default."""
import argparse,copy,importlib.util,json,os,re
from pathlib import Path


def load(name, filename):
 spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(filename));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def prepare(b,images,state,llm_image,cidrs,frontend_image=None,widget_datamapper=None,widget_llm=False,general_knowledge=False):
 r=load('generation_render','render.py')
 if not re.fullmatch(r'ghcr.io/buerokratt/llm-module/central-llm@sha256:[a-f0-9]{64}',llm_image):raise ValueError('immutable_central_llm_image_required')
 if not (state/'installation.json').is_file() or not (state/'credentials.json').is_file() or not (state/'protected-baseline.json').is_file():raise ValueError('existing_installation_and_protected_baseline_required')
 if not all((state/name).is_file() for name in ['engine-ca.crt','engine-ca.key','engine-server.crt','engine-server.key']):raise ValueError('existing_engine_tls_state_required')
 if frontend_image is not None:
  if not re.fullmatch(r'ghcr.io/buerokratt/noops/central-frontend@sha256:[a-f0-9]{64}',frontend_image):raise ValueError('immutable_central_frontend_required')
  images={**images,'frontend':frontend_image}
 if widget_datamapper is not None:
  if not re.fullmatch(r'ghcr.io/buerokratt/datamapper/central-datamapper@sha256:[a-f0-9]{64}',widget_datamapper):raise ValueError('immutable_central_datamapper_required')
  images={**images,'datamapper':widget_datamapper}
  b={**b,'widgetRuntimeFixes':True,'widgetLLMEnabled':widget_llm}
 if general_knowledge:b={**b,'llmGeneralKnowledgeEnabled':True}
 old=json.loads((state/'installation.json').read_text());b={**b,'llmGenerationEnabled':True,'llmProviderCIDRs':cidrs};images={**images,'llm':llm_image}
 wanted,stages,_=r.render(b,images,state)
 identity=lambda o:(o['kind'],o['metadata'].get('namespace'),o['metadata']['name'])
 prior={identity(o):o for o in old['items']};nexts={identity(o):o for o in wanted['items']}
 allowed={('Deployment',r.OWNER,r.OWNER+'-llm'),('Deployment',r.OWNER,r.OWNER+'-notification'),('Service',r.OWNER,r.OWNER+'-backend'),('NetworkPolicy',r.OWNER,'llm-provider-egress')}
 if frontend_image is not None:allowed.add(('Deployment',r.OWNER,r.OWNER+'-frontend'))
 if widget_datamapper is not None:allowed.update({('Deployment',r.OWNER,r.OWNER+'-backend'),('ConfigMap',r.OWNER,'backend-config'),('ConfigMap',r.OWNER,'widget-runtime-fixes')})
 if set(prior)-set(nexts) or any(prior.get(k)!=nexts[k] for k in nexts if k not in allowed):raise ValueError('unrelated_manifest_change_rejected')
 return b,images,wanted,stages,prior,[nexts[k] for k in sorted(allowed)]


def main():
 p=argparse.ArgumentParser(description=__doc__)
 for key in ['bindings','images','kubeconfig','state-dir','llm-image']:p.add_argument('--'+key,required=True)
 p.add_argument('--frontend-image')
 p.add_argument('--widget-datamapper')
 p.add_argument('--enable-widget-llm',action='store_true')
 p.add_argument('--enable-general-knowledge',action='store_true')
 p.add_argument('--provider-cidr',action='append',required=True);p.add_argument('--execute',action='store_true');a=p.parse_args();os.umask(0o077)
 state=Path(a.state_dir).resolve(strict=True)
 if state.stat().st_mode&0o077:raise ValueError('private_state_required')
 binding_path=Path(a.bindings).resolve(strict=True);image_path=Path(a.images).resolve(strict=True)
 old_b=json.loads(binding_path.read_text());old_images=json.loads(image_path.read_text())
 b,images,wanted,stages,prior,targets=prepare(old_b,old_images,state,a.llm_image,a.provider_cidr,a.frontend_image,a.widget_datamapper,a.enable_widget_llm,a.enable_general_knowledge)
 m=load('generation_install','install.py');i=m.Installer(b,a.kubeconfig,state);i.identity();i.preservation(first=False)
 def contract(o):
  if o['kind']=='NetworkPolicy':return o['spec']
  if o['kind']=='Service':
   if o['spec'].get('type','ClusterIP')!='ClusterIP':raise ValueError('service_type_drift')
   ports=[{k:v for k,v in p.items() if not (k=='protocol' and v=='TCP')} for p in o['spec']['ports']]
   return {'selector':o['spec']['selector'],'ports':ports}
  return i.contract(o)
 def observed_variant(o):
  o=copy.deepcopy(o)
  if o['kind']=='Deployment':
   for co in o['spec']['template']['spec']['containers']:
    for e in co.get('env',[]):
     if e['name']=='LLM_GENERATION_ENABLED':e['value']='true'
  elif o['kind']=='Service':
   if not any(p['name']=='resql' for p in o['spec']['ports']):o['spec']['ports'].append({'name':'resql','port':8082,'targetPort':8082})
  return o
 plans=[]
 for target in targets:
  kind=target['kind'];name=target['metadata']['name'];key=(kind,m.OWNER,name);old=prior.get(key)
  live=i.kube(m.OWNER,'get',kind,name,'-o','json',missing=True)
  if not live:
   if kind!='NetworkPolicy' and not (kind=='ConfigMap' and name=='widget-runtime-fixes'):raise ValueError('existing_workload_missing')
   admitted=i.kube(m.OWNER,'create','--dry-run=server','-f','-','-o','json',payload=target)
   if contract(admitted)!=contract(target):raise ValueError('admission_changed_contract')
   plans.append((target,None));continue
  owner=live['metadata'].get('labels',{}).get(m.LABEL)
  if owner!=m.OWNER and not (kind=='NetworkPolicy' and owner is None):raise ValueError('foreign_owner_rejected')
  hashes={target['metadata']['annotations'][m.HASH]}
  if old:hashes.add(old['metadata']['annotations'][m.HASH])
  live_hash=live['metadata'].get('annotations',{}).get(m.HASH)
  if owner==m.OWNER and live_hash not in hashes and not (kind=='NetworkPolicy' and live_hash is None):raise ValueError('creation_hash_drift_'+name)
  accepted=[contract(target)]
  if old:accepted.extend([contract(old),contract(observed_variant(old))])
  if contract(live) not in accepted:raise ValueError('unexpected_live_contract_'+name)
  labels={**live['metadata'].get('labels',{}),m.LABEL:m.OWNER};annotations={**live['metadata'].get('annotations',{}),m.HASH:target['metadata']['annotations'][m.HASH]}
  patch=[{'op':'test','path':'/metadata/resourceVersion','value':live['metadata']['resourceVersion']},{'op':'add','path':'/metadata/labels','value':labels},{'op':'add','path':'/metadata/annotations','value':annotations}]
  if kind=='Deployment':
   containers=copy.deepcopy(live['spec']['template']['spec']['containers'])
   for co,desired in zip(containers,target['spec']['template']['spec']['containers']):
    if co['name']!=desired['name']:raise ValueError('container_order_changed')
    if co['name'] in ['llm','notification','frontend','mapper']:co['image']=desired['image'];co['env']=desired['env']
    if name==m.OWNER+'-backend':co['volumeMounts']=desired.get('volumeMounts',[])
   patch.append({'op':'replace','path':'/spec/template/spec/containers','value':containers})
   if name==m.OWNER+'-backend':patch.append({'op':'replace','path':'/spec/template/spec/volumes','value':target['spec']['template']['spec']['volumes']})
  elif kind=='ConfigMap':patch.append({'op':'add','path':'/data','value':target['data']})
  elif kind=='Service':patch.append({'op':'replace','path':'/spec/ports','value':target['spec']['ports']})
  elif contract(live)!=contract(target):raise ValueError('provider_policy_drift')
  admitted=i.kube(m.OWNER,'patch',kind,name,'--type=json','-p',json.dumps(patch),'--dry-run=server','-o','json')
  if contract(admitted)!=contract(target):raise ValueError('admission_changed_contract')
  plans.append((target,patch))
 print(json.dumps({'status':'GENERATION_UPGRADE_PLAN_PASS','targets':[o['metadata']['name'] for o,_ in plans],'databaseChanges':False,'schemaJobsReplayed':False,'providerHTTPSOnly':True}))
 if not a.execute:return
 backup=state/('before-runtime-upgrade-'+a.llm_image[-12:]);backup.mkdir(mode=0o700,exist_ok=True)
 for name,path in [('bindings.json',binding_path),('images.json',image_path),('installation.json',state/'installation.json'),('stages.json',state/'stages.json')]:
  dest=backup/name
  if not dest.exists():dest.write_bytes(path.read_bytes());dest.chmod(0o600)
 for target,patch in plans:
  if patch is None:actual=i.kube(m.OWNER,'create','-f','-','-o','json',payload=target)
  else:actual=i.kube(m.OWNER,'patch',target['kind'],target['metadata']['name'],'--type=json','-p',json.dumps(patch),'-o','json')
  if contract(actual)!=contract(target):raise ValueError('applied_contract_mismatch')
 # Save existing state only after every scoped patch succeeds. Retry is safe if interrupted.
 for path,value in [(binding_path,b),(image_path,images),(state/'installation.json',wanted),(state/'stages.json',stages)]:
  pending=path.with_name(path.name+'.generation-pending');pending.write_text(json.dumps(value,indent=2)+'\n');pending.chmod(0o600);pending.replace(path)
 for target,_ in plans:i.wait(target)
 i.preservation()
 print(json.dumps({'status':'GENERATION_UPGRADED_PROVIDER_TEST_PENDING','privateBackup':str(backup),'modelGenerationExecuted':False}))

if __name__=='__main__':
 try:main()
 except Exception as exc:
  print(json.dumps({'status':'STOPPED','reason':str(exc) if isinstance(exc,ValueError) or type(exc).__name__=='Stop' else type(exc).__name__}));raise SystemExit(1)
