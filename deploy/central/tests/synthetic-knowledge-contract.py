"""No network/provider calls: test single fixture ownership/schema and repeat safety."""
import copy,importlib.util,json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'deployment/synthetic-knowledge.py';s=importlib.util.spec_from_file_location('synthetic',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
compile(p.read_text().rsplit("\nif __name__=='__main__':",1)[0]+'\nprint(worker(False))','worker','exec')
state={'collection':None,'point':None};calls=[];provider=[]
def request(method,path,body=None,missing=False):
 if method=='GET':
  if '/points/' in path:return copy.deepcopy({'result':state['point']} if state['point'] else None)
  return copy.deepcopy({'result':state['collection']} if state['collection'] else None)
 if path.endswith('/points/count'):return {'result':{'count':int(state['point'] is not None)}}
 calls.append((method,path))
 if '/points?' in path:state['point']=copy.deepcopy(body['points'][0])
 else:state['collection']={'config':{'params':body}}
 return {'status':'ok'}
def embedding(text):provider.append(text);return {'embeddings':[[0.1,0.2,0.3]],'model_used':'synthetic/mock-only'}
assert m.populate(request,embedding)['status']=='SYNTHETIC_KNOWLEDGE_PLAN_PASS' and not calls and not provider
assert m.populate(request,embedding,True)['status']=='SYNTHETIC_KNOWLEDGE_INDEXED'
assert len(provider)==1 and len(calls)==2
assert m.populate(request,embedding,True)['status']=='SYNTHETIC_KNOWLEDGE_REUSED' and len(provider)==1
state['point']['payload']['original_content']='foreign knowledge'
try:m.populate(request,embedding,True)
except ValueError as exc:assert str(exc)=='synthetic_point_conflict'
else:raise AssertionError('foreign point overwritten')
state['point']=None;state['collection']['config']['params']['vectors']['size']=999
before=copy.deepcopy(calls)
try:m.populate(request,embedding,True)
except ValueError as exc:assert str(exc)=='collection_embedding_schema_mismatch'
else:raise AssertionError('incompatible collection changed')
assert calls==before
print(json.dumps({'status':'PASS','planNoProviderOrWrites':True,'singlePointCreated':True,'idempotentNoRepeatProviderCall':True,'foreignPointRejected':True,'schemaMismatchNoWrites':True,'clusterCalls':0}))

# Exercise the actual command transport, not only population logic.
from unittest.mock import patch
from types import SimpleNamespace
code='print("large worker")\n' * 1000
installer=SimpleNamespace(base=['kubectl','--context','rit-byrokratt'])
with patch.object(m.subprocess,'run',return_value=SimpleNamespace(returncode=0,stdout=b'{"status":"SYNTHETIC_KNOWLEDGE_PLAN_PASS"}',stderr=b'')) as run:
 assert m.run_worker(installer,'central-byk-test',code)['status']=='SYNTHETIC_KNOWLEDGE_PLAN_PASS'
 args,kwargs=run.call_args
 assert args[0][-2:]==['/app/.venv/bin/python3','-'] and '-i' in args[0]
 assert code not in args[0] and kwargs['input']==code.encode() and kwargs['capture_output'] is True
with patch.object(m.subprocess,'run',return_value=SimpleNamespace(returncode=1,stdout=b'',stderr=b'414 Request-URI Too Large private-do-not-export')):
 try:m.run_worker(installer,'central-byk-test',code)
 except ValueError as exc:assert str(exc)=='exec_uri_too_large'
 else:raise AssertionError('transport failure ignored')
print(json.dumps({'status':'PASS','largeWorkerUsesStdin':True,'noSourceInExecURI':True,'transportErrorRedacted':True}))
