"""Real-source import scope, idempotence, safe refresh and failure boundaries."""
import copy,hashlib,importlib.util,json
from pathlib import Path
s=importlib.util.spec_from_file_location('official_web',Path(__file__).resolve().parents[1]/'deployment/official-web-import.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
docs=[{'url':url,'text':'Approved official public information. '*5} for url in m.SOURCES]
for d in docs:d['document_hash']=hashlib.sha256(d['text'].encode()).hexdigest()
points={'foreign':{'id':'foreign','payload':{'fixture':'preserve'},'vector':[.2]*3072}}
original=copy.deepcopy(points);calls=[];embeddings=[]
def request(method,path,body=None,missing=False):
 if method=='GET' and path=='/collections/'+m.COLLECTION:return {'result':{'config':{'params':{'vectors':{'size':3072,'distance':'Cosine'}}}}}
 if path.endswith('/points/scroll'):
  assert body['filter']['must'][0]['match']['value']==m.OWNER
  return {'result':{'points':copy.deepcopy([p for p in points.values() if p['payload'].get('official_source_owner')==m.OWNER and p['payload'].get('source_url') in m.SOURCES]),'next_page_offset':None}}
 if method=='GET':
  key=path.rsplit('/',1)[-1]
  if key not in points:
   assert missing
   return None
  return {'result':copy.deepcopy(points[key])}
 calls.append((method,path))
 if method=='PUT':
  for point in body['points']:points[point['id']]=copy.deepcopy(point)
 elif method=='POST' and '/points/delete' in path:
  for key in body['points']:
   assert points[key]['payload']['official_source_owner']==m.OWNER
   del points[key]
 else:raise AssertionError((method,path))
 return {'result':{'status':'completed'}}
def embed(texts):
 embeddings.append(texts)
 return {'embeddings':[[.1]*3072 for _ in texts],'model_used':'fixture-model'}
plan=m.populate(request,embed,docs)
assert not calls and not embeddings and points==original
result=m.populate(request,embed,docs,True,plan['sourceStateFingerprint'])
assert result['status']=='OFFICIAL_WEB_IMPORTED' and len(embeddings)==1 and points['foreign']==original['foreign']
plan=m.populate(request,embed,docs);before=copy.deepcopy(points);n=len(calls)
assert m.populate(request,embed,docs,True,plan['sourceStateFingerprint'])['status']=='OFFICIAL_WEB_REUSED'
assert points==before and len(calls)==n and len(embeddings)==1
changed=copy.deepcopy(docs);changed[0]['text']+=' Current revised source.';changed[0]['document_hash']=hashlib.sha256(changed[0]['text'].encode()).hexdigest()
plan=m.populate(request,embed,changed);assert plan['staleOwnedChunks']==1
result=m.populate(request,embed,changed,True,plan['sourceStateFingerprint'])
assert result['deletedOldOwnedChunks']==1 and points['foreign']==original['foreign']
for url in ['http://www.emta.ee/','https://127.0.0.1/','https://www.emta.ee.evil.test/','https://user:secret@www.emta.ee/']:
 try:m.validate_url(url)
 except ValueError:pass
 else:raise AssertionError('unapproved URL accepted')
parser=m.Text();parser.feed('<nav>ignore</nav><main><h1>Official</h1><script>ignore</script><p>Actual content.</p></main><footer>ignore</footer>');assert parser.text()=='Official Actual content.'
plan=m.populate(request,embed,changed)
try:m.populate(request,embed,changed,True,'foreign-fingerprint')
except ValueError as e:assert str(e)=='source_state_changed_since_plan'
else:raise AssertionError('stale plan accepted')
# Detect a deterministic-ID collision before any embedding or write.
third=copy.deepcopy(changed);third[0]['text']+=' New version';third[0]['document_hash']=hashlib.sha256(third[0]['text'].encode()).hexdigest();target=m.chunks_for(third)[0];points[target['id']]={'id':target['id'],'payload':{'owner':'foreign'},'vector':[.2]*3072};n=len(calls);e=len(embeddings)
try:m.populate(request,embed,third)
except ValueError as exc:assert str(exc)=='source_point_collision'
else:raise AssertionError('foreign deterministic-ID point accepted')
assert len(calls)==n and len(embeddings)==e
print(json.dumps({'status':'PASS','planNoEmbeddingOrWrites':True,'foreignFixturePreserved':True,'idempotentNoRepeatEmbedding':True,'refreshDeletesOnlyStaleOwnedPoints':True,'stalePlanAndCollisionRejected':True,'approvedHTTPSOnly':True,'navigationAndScriptsExcluded':True,'clusterCalls':0}))
