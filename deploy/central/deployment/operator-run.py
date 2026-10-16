#!/usr/bin/env python3
"""Single operator entry point: render once/reuse private state, install, accept."""
import argparse,json,subprocess,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--bindings',required=True);p.add_argument('--images',required=True);p.add_argument('--kubeconfig',required=True);p.add_argument('--state-dir',required=True);p.add_argument('--vault-token-file',required=True);p.add_argument('--execute',action='store_true');p.add_argument('--skip-browser-origin-health',action='store_true');a=p.parse_args()
 state=Path(a.state_dir).expanduser().resolve();state.mkdir(parents=True,mode=0o700,exist_ok=True)
 if state.stat().st_mode&0o077:raise ValueError('private_state_directory_required')
 os.umask(0o077);manifest=state/'installation.json'
 def run(script,*args):subprocess.run([sys.executable,str(ROOT/'deployment'/script),*args],check=True)
 run('render.py','--bindings',a.bindings,'--images',a.images,'--state-dir',str(state),'--output',str(manifest))
 if not a.execute:
  run('operator-vault.py','--bindings',a.bindings,'--kubeconfig',a.kubeconfig)
  print(json.dumps({'status':'PLAN_RENDERED','operatorExecutionRequired':True,'privateManifest':str(manifest),'noClusterMutation':True}));return
 run('install.py','--bindings',a.bindings,'--kubeconfig',a.kubeconfig,'--state-dir',str(state),'--manifest',str(manifest),'--vault-token-file',a.vault_token_file,'--execute')
 pending=a.skip_browser_origin_health or json.loads(Path(a.bindings).read_text()).get('frontendAccessMode','ingress')=='port-forward'
 if not pending:run('health.py','--bindings',a.bindings,'--kubeconfig',a.kubeconfig,'--state-dir',str(state))
 print(json.dumps({'status':'INSTALLED_HEALTH_ACCEPTED' if not pending else 'INSTALLED_ORIGIN_ACCEPTANCE_PENDING','context':'rit-byrokratt','namespace':'central-byk-test','generationEnabled':json.loads(Path(a.bindings).read_text()).get('llmGenerationEnabled',False),'preservedExistingVault':True}))
if __name__=='__main__':
 try:main()
 except (ValueError,subprocess.CalledProcessError) as e:print('Stopped:',type(e).__name__);raise SystemExit(1)
