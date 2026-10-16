#!/usr/bin/env python3
"""Operator acceptance: fresh test login/routes and dependency health, no generation."""
import argparse,json,ssl,subprocess,urllib.request,urllib.error,http.cookies
from pathlib import Path
from urllib.parse import urlsplit
class Stop(Exception):pass
def main():
 p=argparse.ArgumentParser();p.add_argument('--bindings',required=True);p.add_argument('--kubeconfig',required=True);p.add_argument('--state-dir',required=True);p.add_argument('--loopback-origin');a=p.parse_args();b=json.loads(Path(a.bindings).read_text());state=Path(a.state_dir)
 if b.get('context')!='rit-byrokratt' or b.get('applicationNamespace')!='central-byk-test':raise Stop('target_scope_mismatch')
 if state.stat().st_mode&0o077:raise Stop('private_state_required')
 origin=b['frontendOrigin']
 if a.loopback_origin:
  parsed=urlsplit(a.loopback_origin)
  if parsed.scheme!='http' or parsed.hostname not in ['localhost','127.0.0.1'] or parsed.username or parsed.password or parsed.path not in ['','/']:raise Stop('only_explicit_loopback_forward_allowed')
  origin=a.loopback_origin.rstrip('/')
 elif urlsplit(origin).scheme!='https':raise Stop('verified_frontend_TLS_required')
 base=['kubectl','--kubeconfig',str(Path(a.kubeconfig).resolve(strict=True)),'--context','rit-byrokratt','--namespace','central-byk-test','--request-timeout=30s']
 def kube(*args):
  r=subprocess.run(base+list(args),capture_output=True,timeout=40)
  if r.returncode:raise Stop('task_kubernetes_probe_failed')
  return json.loads(r.stdout)
 v=kube('config','view','--minify','-o','json')
 if v['clusters'][0]['cluster']['server']!=b['expectedAPIServer'] or kube('get','namespace','kube-system','-o','json')['metadata']['uid']!=b['expectedKubeSystemUID']:raise Stop('cluster_identity_mismatch')
 for name in ['central-byk-test-backend','central-byk-test-llm','central-byk-test-knowledge','central-byk-test-frontend']:
  obj=kube('get','deployment',name,'-o','json')
  if obj['metadata'].get('labels',{}).get('buerokratt.ee/deployment')!='central-byk-test' or obj.get('status',{}).get('availableReplicas',0)!=1:raise Stop('task_deployment_not_ready_'+name)
 user=json.loads((state/'credentials.json').read_text())['testUser'];cookie=None;checks=[]
 class NoRedirect(urllib.request.HTTPRedirectHandler):
  def redirect_request(self,*args,**kwargs):raise Stop('frontend_redirect_refused')
 opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect(),urllib.request.HTTPSHandler(context=ssl.create_default_context(cafile=b.get('frontendCAFile') or None)))
 def req(path,body=None,expect=200):
  nonlocal cookie
  headers={'Content-Type':'application/json'}
  if cookie:headers['Cookie']=cookie
  request=urllib.request.Request(origin+path,method='GET' if body is None else 'POST',data=None if body is None else json.dumps(body).encode(),headers=headers)
  try:
   with opener.open(request,timeout=30) as response:status=response.status;raw=response.read(1048577);setcookie=response.headers.get('Set-Cookie')
  except urllib.error.HTTPError as e:status=e.code;raw=e.read(1048577);setcookie=None;e.close()
  if status!=expect:raise Stop('frontend_probe_status_'+str(status)+'_'+path.replace('/','_'))
  if len(raw)>1048576:raise Stop('frontend_response_limit')
  if setcookie:
   parsed=http.cookies.SimpleCookie();parsed.load(setcookie)
   if 'customJwtCookie' not in parsed or not parsed['customJwtCookie']['httponly']:raise Stop('http_only_session_required')
   cookie='customJwtCookie='+parsed['customJwtCookie'].value
  try:return json.loads(raw)
  except ValueError:return None
 req('/api/public/backoffice/auth/login',{'login':user['login'],'password':'deliberately-invalid'},400);checks.append('wrong_password_rejected')
 req('/api/public/backoffice/auth/login',user)
 if not cookie:raise Stop('login_session_not_returned')
 info=req('/api/private/backoffice/auth/jwt/userinfo')
 payload=info.get('response',info) if isinstance(info,dict) else None
 if not isinstance(payload,dict) or payload.get('idCode')!=user['login']:raise Stop('fresh_test_identity_mismatch')
 checks.append('real_TIM_authenticated_fresh_test_user')
 req('/api/private/services/slots');checks.append('real_Service_inline_template_route')
 # Exec only explicit task deployments; these endpoints neither generate nor write data.
 llm=kube('exec','deployment/central-byk-test-llm','-c','llm','--','/app/.venv/bin/python3','-c',"import json,urllib.request;print(json.dumps(json.load(urllib.request.urlopen('http://127.0.0.1:8100/health'))))")
 if llm.get('generation_enabled') is not False or llm.get('redis_session_store')!='connected':raise Stop('LLM_non_generating_storage_health_failed')
 checks.append('LLM_generation_disabled_Redis_connected')
 ckb=kube('exec','deployment/central-byk-test-knowledge','-c','knowledge','--','node','-e',"fetch('http://127.0.0.1:3000/health').then(async r=>{if(!r.ok)process.exit(1);console.log(JSON.stringify(await r.json()))}).catch(()=>process.exit(1))")
 if ckb.get('status')!='healthy':raise Stop('knowledge_engine_health_failed')
 checks.append('real_knowledge_scoped_engine_health')
 print(json.dumps({'status':'PASS','checks':checks,'generationExecuted':False,'historicStateCopied':False,'cookieValuesExported':False}))
if __name__=='__main__':
 try:main()
 except (Stop,OSError,ValueError) as e:print(json.dumps({'status':'STOPPED','reason':str(e) if isinstance(e,Stop) else type(e).__name__}));raise SystemExit(1)
