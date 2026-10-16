"""Create/verify only fresh-installation scoped engine resources; no historic data."""
import base64,json,os,ssl
from pathlib import Path
from urllib.request import Request,build_opener,ProxyHandler,HTTPSHandler,HTTPRedirectHandler
from urllib.error import HTTPError
OWNER='central-byk-test'
class Stop(Exception):pass
class NoRedirect(HTTPRedirectHandler):
 def redirect_request(self,*args,**kw):raise Stop('redirect_refused')
def main():
 origin=os.environ['OPENSEARCH_URL'];auth={k:Path('/run/bootstrap/'+k).read_text() for k in ['username','password']}
 if not origin.startswith('https://'):raise Stop('verified_TLS_required')
 opener=build_opener(ProxyHandler({}),NoRedirect(),HTTPSHandler(context=ssl.create_default_context(cafile='/engine-ca/ca.crt')))
 def api(method,path,body=None,missing=False,account=auth):
  req=Request(origin+path,method=method,data=None if body is None else json.dumps(body).encode(),headers={'Content-Type':'application/json','Authorization':'Basic '+base64.b64encode((account['username']+':'+account['password']).encode()).decode()})
  try:
   with opener.open(req,timeout=20) as r:
    raw=r.read(8388609)
    if len(raw)>8388608:raise Stop('response_limit')
    return json.loads(raw or '{}')
  except HTTPError as e:
   code=e.code;e.close()
   if missing and code==404:return None
   raise Stop('engine_http_'+str(code)) from None
 read=['indices:data/read/*','indices:admin/exists','indices:admin/get','indices:admin/refresh*']
 definitions={
 'chatbot':(['notifications','chatqueue'],['indices:data/write/bulk'],read+['indices:admin/mapping/put','indices:data/write/index*','indices:data/write/update*','indices:data/write/delete*','indices:data/write/bulk*','indices:data/write/delete/byquery*']),
 'common':(['companies','municipalities'],['indices:data/write/bulk','indices:data/read/mget'],read+['indices:data/write/index*','indices:data/write/bulk*']),
 'service':(['domain','rules','services'],[],read+['indices:admin/mapping/put','indices:data/write/index*','indices:data/write/delete*','indices:data/write/bulk*']),
 'knowledge':(['*'],['cluster:monitor/health','indices:data/write/bulk'],read+['indices:admin/create','indices:admin/delete','indices:admin/mapping/put','indices:data/write/index*','indices:data/write/bulk*','indices:data/write/delete*']),
 'logging':(['ruuterlog'],[],['indices:admin/mapping/put','indices:data/write/index*','indices:data/write/bulk*'])}
 for name,(suffixes,cluster,actions) in definitions.items():
  role=OWNER+'-'+name;body={'cluster_permissions':cluster,'index_permissions':[{'index_patterns':[OWNER+'-'+name+'-'+s for s in suffixes],'allowed_actions':actions}],'tenant_permissions':[]}
  if name=='service':body['index_permissions'].append({'index_patterns':[OWNER+'-logging-ruuterlog'],'allowed_actions':['indices:data/read/*']})
  path='/_plugins/_security/api/roles/'+role;existing=api('GET',path,missing=True)
  if existing is None:api('PUT',path,body)
  else:
   current=existing.get(role,{})
   if any(current.get(k,[])!=v for k,v in body.items()):raise Stop('role_conflict_'+name)
  account={k:Path('/run/'+name+'/'+k).read_text() for k in ['username','password']};path='/_plugins/_security/api/internalusers/'+account['username'];existing=api('GET',path,missing=True)
  if existing is None:api('PUT',path,{'password':account['password'],'opendistro_security_roles':[role],'backend_roles':[],'attributes':{}})
  elif existing.get(account['username'],{}).get('opendistro_security_roles')!=[role]:raise Stop('user_role_conflict_'+name)
  info=api('GET','/_plugins/_security/authinfo',account=account)
  if info.get('user_name')!=account['username']:raise Stop('account_authentication_failed')
 schemas=json.loads(Path('/config/indices.json').read_text())
 for index,mapping in schemas.items():
  if not index.startswith(OWNER+'-'):raise Stop('schema_scope')
  existing=api('GET','/'+index+'/_mapping',missing=True)
  if existing is None:api('PUT','/'+index,{'settings':{'number_of_shards':1,'number_of_replicas':0},'mappings':mapping})
  else:
   actual=existing[index]['mappings']
   def includes(want,got):return all(k in got and (includes(v,got[k]) if isinstance(v,dict) else v==got[k]) for k,v in want.items())
   if not includes(mapping,actual):raise Stop('schema_conflict_'+index)
 print(json.dumps({'status':'PASS','scopedAccounts':5,'freshIndices':len(schemas),'existingResourcesOverwritten':False}))
if __name__=='__main__':
 try:main()
 except (Stop,OSError,ValueError) as e:print(json.dumps({'status':'FAIL','reason':str(e) if isinstance(e,Stop) else type(e).__name__}));raise SystemExit(1)
