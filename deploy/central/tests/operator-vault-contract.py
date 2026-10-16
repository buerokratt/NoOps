import importlib.util,json,subprocess,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('provisioner',root/'deployment/operator-vault.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
policies=m.policies('secret');assert len(policies)==9
for name,policy in policies.items():
 assert 'path "*"' not in policy
 assert 'central-byk-test/' in policy
 assert 'sys/' not in policy
 if name.endswith('-gui'):
  assert 'encryption/public_key" { capabilities = ["read"]' in policy
  assert 'encryption/private_key" { capabilities = ["deny"]' in policy
 if '-delivery' in name:assert '"read"' in policy.splitlines()[0] and '"update"' not in policy.splitlines()[0]
for value in ['../secret','secret/other','',None]:
 try:m.segment(value)
 except m.Stop:pass
 else:raise AssertionError('invalid mount accepted')
with tempfile.TemporaryDirectory() as tmp:
 binding=Path(tmp)/'binding.json'
 for data in [{'context':'rit-byrokratt-stage'},{'context':'rit-byrokratt','applicationNamespace':'central-byk-test'}]:
  binding.write_text(json.dumps(data));r=subprocess.run(['python3',str(root/'deployment/operator-vault.py'),'--bindings',str(binding),'--kubeconfig','/nonexistent'],capture_output=True)
  assert r.returncode==1 and b'Stopped:' in r.stdout
print(json.dumps({'status':'PASS','policyContracts':9,'unboundAndWrongContextReject':True,'invalidMountReject':True,'runtimeIntegration':'separate local-adapter test'}))
