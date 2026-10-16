#!/usr/bin/env python3
"""Operator-only single synthetic RAG reference; no imports or application seed replay."""
import argparse,contextlib,hashlib,importlib.util,io,json,math,os,re,subprocess,uuid,urllib.request,urllib.error
from pathlib import Path
COLLECTION='contextual_chunks_azure'
POINT_ID=str(uuid.uuid5(uuid.NAMESPACE_URL,'central-byk-test:synthetic-library-reference:v1'))
TEXT=('Synthetic acceptance reference for the fictional Central Test municipal library. '
      'The Central Test municipal library lends books, provides study spaces, and offers free public computer access. '
      'Its synthetic help desk opens Monday through Friday from 09:00 to 17:00. '
      'This reference is test data, not a statement about a real institution.')
PAYLOAD={'acceptance_owner':'central-byk-test','fixture_version':1,'chunk_id':POINT_ID,
         'document_hash':hashlib.sha256(TEXT.encode()).hexdigest(),'original_content':TEXT,
         'contextual_content':TEXT,'context_only':'Fictional Central Test municipal library acceptance reference.',
         'document_url':'https://example.invalid/central-test-library','chunk_index':0,'total_chunks':1}


def populate(request,embedding,execute=False):
 info=request('GET','/collections/'+COLLECTION,missing=True)
 existing=None
 if info:
  existing=request('GET','/collections/'+COLLECTION+'/points/'+POINT_ID,missing=True)
  if existing:
   if any(existing['result'].get('payload',{}).get(k)!=v for k,v in PAYLOAD.items()):raise ValueError('synthetic_point_conflict')
  count=request('POST','/collections/'+COLLECTION+'/points/count',{'exact':True})['result']['count']
  if count!=(1 if existing else 0):raise ValueError('collection_contains_other_knowledge_stop')
 if not execute:return {'status':'SYNTHETIC_KNOWLEDGE_PLAN_PASS','existingFixture':bool(existing),'providerCalls':0,'pointID':POINT_ID}
 if existing:return {'status':'SYNTHETIC_KNOWLEDGE_REUSED','pointID':POINT_ID,'providerCalls':0}
 result=embedding(TEXT);vectors=result.get('embeddings',[])
 if len(vectors)!=1 or not vectors[0] or not all(isinstance(x,(float,int)) and math.isfinite(x) for x in vectors[0]):raise ValueError('invalid_provider_embedding')
 vector=vectors[0]
 if info:
  config=info['result']['config']['params']['vectors']
  if config.get('size')!=len(vector) or config.get('distance')!='Cosine':raise ValueError('collection_embedding_schema_mismatch')
 else:request('PUT','/collections/'+COLLECTION,{'vectors':{'size':len(vector),'distance':'Cosine'}})
 payload={**PAYLOAD,'embedding_model':result['model_used']}
 request('PUT','/collections/'+COLLECTION+'/points?wait=true',{'points':[{'id':POINT_ID,'vector':vector,'payload':payload}]})
 saved=request('GET','/collections/'+COLLECTION+'/points/'+POINT_ID)['result']
 if any(saved['payload'].get(k)!=v for k,v in payload.items()):raise ValueError('fixture_verification_failed')
 return {'status':'SYNTHETIC_KNOWLEDGE_INDEXED','pointID':POINT_ID,'dimensions':len(vector),'providerCalls':1}


def worker(execute):
 opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
 def request(method,path,body=None,missing=False,base='http://central-byk-test-qdrant:6333'):
  req=urllib.request.Request(base+path,method=method,data=None if body is None else json.dumps(body).encode(),headers={'Content-Type':'application/json'})
  try:
   with opener.open(req,timeout=120) as response:return json.load(response)
  except urllib.error.HTTPError as exc:
   if missing and exc.code==404:return None
   raise ValueError('task_endpoint_http_'+str(exc.code)) from None
 def embedding(text):
  with contextlib.redirect_stdout(io.StringIO()):
   from src.utils.connection_id_fetcher import get_connection_id_fetcher
   connection=get_connection_id_fetcher().fetch_vault_uuid_sync('testing')
  if not connection:raise ValueError('testing_connection_required')
  return request('POST','/embeddings',{'texts':[text],'environment':'testing','connection_id':connection,'batch_size':1},base='http://127.0.0.1:8100')
 return populate(request,embedding,execute)


def run_worker(installer,namespace,code):
 # Keep source out of exec URL query arguments: Rancher/proxies limit URI size.
 command=installer.base+['--namespace',namespace,'exec','-i','deployment/central-byk-test-llm','-c','llm','--','/app/.venv/bin/python3','-']
 try:completed=subprocess.run(command,input=code.encode(),capture_output=True,timeout=240)
 except subprocess.TimeoutExpired:raise ValueError('fixture_worker_timeout') from None
 if completed.returncode:
  # Never echo stderr: kubectl/provider failures may contain private data.
  error=completed.stderr.decode(errors='replace').lower()
  reason=next((label for token,label in [('request-uri too large','exec_uri_too_large'),('414','exec_uri_too_large'),('forbidden','exec_forbidden'),('not found','exec_target_not_found'),('unable to upgrade connection','exec_upgrade_failed')] if token in error),'exec_transport_failed')
  raise ValueError(reason)
 try:return json.loads(completed.stdout)
 except ValueError:raise ValueError('fixture_worker_non_json_output') from None


def main():
 p=argparse.ArgumentParser(description=__doc__)
 for key in ['bindings','kubeconfig','state-dir']:p.add_argument('--'+key,required=True)
 p.add_argument('--execute',action='store_true');p.add_argument('--package');a=p.parse_args();state=Path(a.state_dir)
 if state.stat().st_mode&0o077:raise ValueError('private_state_required')
 installer_file=Path(a.package).resolve(strict=True)/'deployment/install.py' if a.package else Path(__file__).with_name('install.py')
 spec=importlib.util.spec_from_file_location('fixture_installer',installer_file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 binding=json.loads(Path(a.bindings).read_text())
 if binding.get('llmGenerationEnabled') is not True:raise ValueError('enabled_generation_binding_required')
 i=m.Installer(binding,a.kubeconfig,state);i.identity();i.preservation(first=False)
 manifest=json.loads((state/'installation.json').read_text())['items']
 for kind,name in [('Deployment','central-byk-test-llm'),('StatefulSet','central-byk-test-qdrant'),('Service','central-byk-test-qdrant')]:
  expected=next(o for o in manifest if o['kind']==kind and o['metadata']['name']==name and o['metadata'].get('namespace')==m.OWNER)
  live=i.kube(m.OWNER,'get',kind,name,'-o','json')
  if live['metadata'].get('labels',{}).get(m.LABEL)!=m.OWNER or i.contract(live)!=i.contract(expected):raise ValueError('task_ownership_or_contract_mismatch')
  if kind=='Service' and live['spec']['selector']!=expected['spec']['selector']:raise ValueError('qdrant_service_selector_mismatch')
 # Transport only this reviewed script into the task LLM container; no host shell.
 source=Path(__file__).read_text().rsplit("\nif __name__=='__main__':",1)[0]
 code=source+'\ntry: print(json.dumps(worker('+repr(a.execute)+')))\nexcept Exception as exc: print(json.dumps({"status":"STOPPED","reason":str(exc) if re.fullmatch(r"(?:task_endpoint_http_[0-9]{3}|synthetic_point_conflict|collection_contains_other_knowledge_stop|collection_embedding_schema_mismatch|fixture_verification_failed|testing_connection_required|invalid_provider_embedding)",str(exc)) else type(exc).__name__}))\n'
 result=run_worker(i,m.OWNER,code)
 if not result or result.get('status') not in ['SYNTHETIC_KNOWLEDGE_PLAN_PASS','SYNTHETIC_KNOWLEDGE_REUSED','SYNTHETIC_KNOWLEDGE_INDEXED']:raise ValueError('fixture_operation_failed_'+str((result or {}).get('reason','unknown')))
 i.preservation(first=False);print(json.dumps(result))

if __name__=='__main__':
 try:main()
 except Exception as exc:
  print(json.dumps({'status':'STOPPED','reason':str(exc) if isinstance(exc,ValueError) or type(exc).__name__=='Stop' else type(exc).__name__}));raise SystemExit(1)
