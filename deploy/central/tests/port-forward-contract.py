"""Verify loopback access guards and operator sequencing without cluster calls."""
import contextlib,importlib.util,io,json,shutil,subprocess,sys,tempfile
from pathlib import Path
from unittest.mock import patch
root=Path(__file__).resolve().parents[1]
def load(name,file):
 spec=importlib.util.spec_from_file_location(name,root/'deployment'/file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
installer=load('pf_installer','install.py');health=load('pf_health','health.py')
with tempfile.TemporaryDirectory() as td:
 state=Path(td);k=state/'kubeconfig';k.write_text('test fixture')
 b={'context':'rit-byrokratt','applicationNamespace':'central-byk-test','frontendAccessMode':'port-forward','frontendOrigin':'http://localhost:18080','expectedAPIServer':'https://test.invalid','expectedKubeSystemUID':'system','expectedCentralNamespaceUID':'central','storageClass':'storage'}
 i=installer.Installer(b,str(k),state);calls=[]
 def kube(ns,*args,**kwargs):
  calls.append(args)
  if args[0]=='config':return {'clusters':[{'cluster':{'server':b['expectedAPIServer']}}]}
  if args[:2]==('get','namespace'):return {'metadata':{'uid':b['expectedKubeSystemUID'] if args[2]=='kube-system' else b['expectedCentralNamespaceUID']}}
  if args[:2]==('get','storageclass'):return {'provisioner':'fixture.dynamic.storage'}
  raise AssertionError('unnecessary ingress/cluster call:'+str(args))
 i.kube=kube;i.identity();assert len(calls)==4
 for origin in ['http://example.invalid','http://localhost.evil.invalid','http://user@localhost','http://localhost/path','http://localhost?query=x']:
  bad={**b,'frontendOrigin':origin}
  try:installer.Installer(bad,str(k),state)
  except installer.Stop:pass
  else:raise AssertionError('installer accepted non-loopback origin')
  binding=state/'binding.json';binding.write_text(json.dumps(bad))
  args=['health.py','--bindings',str(binding),'--kubeconfig',str(k),'--state-dir',str(state)]
  with patch.object(sys,'argv',args),patch.object(health.subprocess,'run',side_effect=AssertionError('unexpected cluster call')):
   try:health.main()
   except health.Stop:pass
   else:raise AssertionError('health accepted non-loopback origin')
 # Execute operator CLI with subprocess sentinels, proving no pre-tunnel health
 # attempt and no false health-accepted status in port-forward mode.
 dep=state/'package/deployment';dep.mkdir(parents=True)
 shutil.copy2(root/'deployment/operator-run.py',dep/'operator-run.py')
 for script in ['render.py','install.py','operator-vault.py']:(dep/script).write_text('print("offline sentinel")\n')
 (dep/'health.py').write_text('raise SystemExit(91)\n')
 binding=state/'binding.json';binding.write_text(json.dumps(b))
 args=[sys.executable,str(dep/'operator-run.py'),'--bindings',str(binding),'--images','fixture','--kubeconfig',str(k),'--state-dir',str(state),'--vault-token-file','not-read','--execute']
 result=subprocess.run(args,text=True,capture_output=True);assert result.returncode==0,result.stdout+result.stderr
 assert json.loads(result.stdout.splitlines()[-1])['status']=='INSTALLED_ORIGIN_ACCEPTANCE_PENDING'
 binding.write_text(json.dumps({**b,'frontendAccessMode':'ingress','frontendOrigin':'https://test.invalid'}))
 result=subprocess.run(args,text=True,capture_output=True);assert result.returncode==1,'ingress health failure was ignored'
print(json.dumps({'status':'PASS','portForwardSkipsIngressDiscovery':True,'loopbackGuardNegatives':5,'healthDeferredUntilTunnel':True,'ingressHealthStillRequired':True,'clusterCalls':0}))
