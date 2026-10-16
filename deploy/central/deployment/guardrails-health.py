#!/usr/bin/env python3
"""Read-only wait for a specific environment's fully preloaded guardrails."""
import argparse,importlib.util,json,os,time
from pathlib import Path

def ready(health,environment,require_general=False):
 return (health.get('generation_enabled') is True and health.get('guardrails_embedding_loaded') is True
         and health.get('guardrails_loaded') is True and environment in health.get('guardrails_environments',[])
         and health.get('redis_session_store')=='connected'
         and (not require_general or health.get('general_knowledge_enabled') is True))

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for n in ['bindings','kubeconfig','state-dir']:p.add_argument('--'+n,required=True)
 p.add_argument('--environment',choices=['testing','production'],default='testing')
 p.add_argument('--require-general-knowledge',action='store_true')
 p.add_argument('--wait-seconds',type=int,default=180);a=p.parse_args();os.umask(0o077)
 if not 0<=a.wait_seconds<=600:raise ValueError('invalid_wait_seconds')
 spec=importlib.util.spec_from_file_location('guardrails_install',Path(__file__).with_name('install.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 state=Path(a.state_dir).resolve(strict=True)
 if state.stat().st_mode&0o077:raise ValueError('private_state_required')
 i=m.Installer(json.loads(Path(a.bindings).read_text()),a.kubeconfig,state);i.identity();i.preservation(first=False)
 worker="import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8100/health',timeout=5).read().decode())"
 deadline=time.monotonic()+a.wait_seconds
 while True:
  try:health=i.kube(m.OWNER,'exec','deployment/'+m.OWNER+'-llm','-c','llm','--','/app/.venv/bin/python','-c',worker)
  except m.Stop:health={}
  if ready(health or {},a.environment,a.require_general_knowledge):
   print(json.dumps({'status':'GUARDRAILS_PRELOAD_PASS','environment':a.environment,'loadedEnvironments':health['guardrails_environments'],'redis':'connected','generalKnowledgeEnabled':health.get('general_knowledge_enabled',False),'modelGenerationExecuted':False}));return
  if time.monotonic()>=deadline:raise ValueError('guardrails_preload_not_ready_'+a.environment)
  time.sleep(min(3,max(0,deadline-time.monotonic())))

if __name__=='__main__':
 try:main()
 except Exception as exc:
  print(json.dumps({'status':'STOPPED','reason':str(exc) if isinstance(exc,ValueError) or type(exc).__name__=='Stop' else type(exc).__name__}));raise SystemExit(1)
