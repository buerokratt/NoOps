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
