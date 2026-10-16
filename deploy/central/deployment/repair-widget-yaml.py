#!/usr/bin/env python3
"""Repair only the known widget-domain YAML quoting defect in an existing install."""
import argparse,copy,hashlib,importlib.util,json,os,sys
from pathlib import Path
BAD='      userDomains: ${user_domains.response.body?.[0] ?? {"domains": [], "selected": []}}'
GOOD='      userDomains: ${user_domains.response.body?.[0] ?? Object.fromEntries([["domains", []], ["selected", []]])}'
def corrected(manifest):
 result=copy.deepcopy(manifest)
 cm=next(o for o in result['items'] if o['kind']=='ConfigMap' and o['metadata']['name']=='widget-runtime-fixes')
 text=cm['data']['private-2']
 if BAD in text:
  assert text.count(BAD)==1
  cm['data']['private-2']=text.replace(BAD,GOOD)
 elif GOOD not in text:raise ValueError('unknown_widget_override_rejected')
 cm['metadata']['annotations'].pop('buerokratt.ee/creation-sha256',None)
 cm['metadata']['annotations']['buerokratt.ee/creation-sha256']=hashlib.sha256(json.dumps(cm,sort_keys=True).encode()).hexdigest()
 return result,cm

def load(package):
 spec=importlib.util.spec_from_file_location('widget_repair_install',package/'deployment/install.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for n in ['package','bindings','kubeconfig','state-dir']:p.add_argument('--'+n,required=True)
 p.add_argument('--execute',action='store_true');a=p.parse_args();os.umask(0o077)
 package=Path(a.package).resolve(strict=True);state=Path(a.state_dir).resolve(strict=True)
 if state.stat().st_mode&0o077:raise ValueError('private_state_required')
 m=load(package)
 b=json.loads(Path(a.bindings).read_text());i=m.Installer(b,a.kubeconfig,state);i.identity();i.preservation(first=False)
 saved=state/'installation.json';raw=saved.read_bytes();old=json.loads(raw);wanted,cm=corrected(old)
 prior=next(o for o in old['items'] if o['kind']=='ConfigMap' and o['metadata']['name']=='widget-runtime-fixes')
 deployment=next(o for o in old['items'] if o['kind']=='Deployment' and o['metadata']['name']==m.OWNER+'-backend')
 live=i.kube(m.OWNER,'get','ConfigMap','widget-runtime-fixes','-o','json')
 backend=i.kube(m.OWNER,'get','Deployment',m.OWNER+'-backend','-o','json')
 for obj,expected in [(live,prior),(backend,deployment)]:
  if obj['metadata'].get('labels',{}).get(m.LABEL)!=m.OWNER:raise ValueError('foreign_owner_rejected')
  hashes={expected['metadata']['annotations'][m.HASH]}
  if obj is live:hashes.add(cm['metadata']['annotations'][m.HASH])
  if obj['metadata'].get('annotations',{}).get(m.HASH) not in hashes:raise ValueError('creation_hash_drift')
 if i.contract(live) not in [i.contract(prior),i.contract(cm)]:raise ValueError('unrelated_config_drift')
 if i.contract(backend)!=i.contract(deployment):raise ValueError('unrelated_backend_drift')
 cm_patch=[{'op':'test','path':'/metadata/resourceVersion','value':live['metadata']['resourceVersion']},{'op':'add','path':'/data','value':cm['data']},{'op':'add','path':'/metadata/annotations','value':{**live['metadata'].get('annotations',{}),m.HASH:cm['metadata']['annotations'][m.HASH]}}]
 annotations={**backend['spec']['template']['metadata'].get('annotations',{}),'buerokratt.ee/widget-yaml-repair':hashlib.sha256(GOOD.encode()).hexdigest()}
 restart=[{'op':'test','path':'/metadata/resourceVersion','value':backend['metadata']['resourceVersion']},{'op':'add','path':'/spec/template/metadata/annotations','value':annotations}]
 for kind,name,patch,expected in [('ConfigMap','widget-runtime-fixes',cm_patch,cm),('Deployment',m.OWNER+'-backend',restart,deployment)]:
  admitted=i.kube(m.OWNER,'patch',kind,name,'--type=json','-p',json.dumps(patch),'--dry-run=server','-o','json')
  if i.contract(admitted)!=i.contract(expected):raise ValueError('admission_changed_contract')
 print(json.dumps({'status':'WIDGET_YAML_REPAIR_PLAN_PASS','targets':['ConfigMap/widget-runtime-fixes','Deployment/'+m.OWNER+'-backend'],'databaseChanges':False,'imageChanges':False,'schemaJobsReplayed':False}))
 if not a.execute:return
 backup=state/'before-widget-yaml-repair';backup.mkdir(mode=0o700,exist_ok=True)
 dest=backup/'installation.json'
 if not dest.exists():dest.write_bytes(raw);dest.chmod(0o600)
 applied=i.kube(m.OWNER,'patch','ConfigMap','widget-runtime-fixes','--type=json','-p',json.dumps(cm_patch),'-o','json')
 if i.contract(applied)!=i.contract(cm):raise ValueError('applied_config_mismatch')
 pending=state/'installation.json.widget-repair-pending';pending.write_text(json.dumps(wanted,indent=2)+'\n');pending.chmod(0o600);pending.replace(saved)
 applied=i.kube(m.OWNER,'patch','Deployment',m.OWNER+'-backend','--type=json','-p',json.dumps(restart),'-o','json')
 if i.contract(applied)!=i.contract(deployment):raise ValueError('applied_backend_mismatch')
 i.wait(deployment);i.preservation()
 print(json.dumps({'status':'WIDGET_YAML_REPAIRED','databaseChanges':False,'imageChanges':False,'schemaJobsReplayed':False}))

if __name__=='__main__':
 try:main()
 except Exception as exc:
  print(json.dumps({'status':'STOPPED','reason':str(exc) if isinstance(exc,ValueError) or type(exc).__name__=='Stop' else type(exc).__name__}));raise SystemExit(1)
