"""Per-workload alias transport: credential files, verified TLS, no retries."""
import base64,json,os,re,ssl
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request,ProxyHandler,HTTPSHandler,HTTPRedirectHandler,build_opener
from urllib.error import HTTPError
config=json.loads(Path(os.environ['ADAPTER_CONFIG']).read_text());origin=config['origin'].rstrip('/');url=urlsplit(origin)
assert url.scheme in ('https','http') and url.hostname and not url.username and not url.password and not url.query and not url.fragment and url.path in ('','/')
assert url.scheme=='https' or config.get('allowHTTP') is True
aliases=config['aliases'];assert aliases and all(re.fullmatch(r'[a-z0-9_-]+',a) and re.fullmatch(r'central-byk-test-[a-z0-9_-]+',b) for a,b in aliases.items())
templates={p.stem:json.loads(p.read_text())['script']['source'] for directory in config.get('templateDirectories',[]) for p in Path(directory).glob('*.json')}
class NoRedirect(HTTPRedirectHandler):
 def redirect_request(self,*args,**kw):raise ValueError('redirect_refused')
opener=build_opener(ProxyHandler({}),NoRedirect(),HTTPSHandler(context=ssl.create_default_context(cafile=config.get('caFile'))))
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def handle_call(self):
  try:
   parsed=urlsplit(self.path);parts=parsed.path.split('/')[1:]
   if self.command=='GET' and self.path=='/health':return self.reply(200,b'{"status":"ok"}')
   if not parts or parts[0] not in aliases or any(not re.fullmatch(r'[A-Za-z0-9_.-]+',p) or p in ('.','..') for p in parts):return self.reply(403,b'{"error":"scope_denied"}')
   if self.headers.get('Transfer-Encoding'):return self.reply(400,b'{"error":"content_length_required"}')
   length=int(self.headers.get('Content-Length','0'))
   if not 0<=length<=16*1024*1024:return self.reply(413,b'{"error":"request_limit"}')
   body=self.rfile.read(length)
   if config.get('metadataLogging') and self.command=='POST':
    event=json.loads(body);keys=['timestamp','level','dslName','dslMethod','stepName','statusCode','errorCode']
    event={key:(value[:128] if isinstance(value,str) else value) for key,value in event.items() if key in keys and isinstance(value,(str,int,float,type(None)))}
    event.update(requestParams={},requestHeaders={},requestBody={},message='event metadata only',stackTrace=[])
    body=json.dumps(event).encode()
   kind=self.headers.get('Content-Type','application/json')
   if len(parts)>1 and parts[1]=='_search' and len(parts)>2 and parts[2]=='template':
    value=json.loads(body);identifier=value.pop('id',None)
    if identifier not in templates:return self.reply(403,b'{"error":"unknown_template"}')
    if set(value)-{'params'}:return self.reply(400,b'{"error":"template_contract"}')
    body=json.dumps({'source':templates[identifier],**value}).encode()
   if len(parts)>1 and parts[1]=='_bulk':
    lines=body.decode().splitlines();updated=[];i=0
    while i<len(lines):
     action=json.loads(lines[i]);i+=1
     if len(action)!=1:raise ValueError('action')
     op,metadata=next(iter(action.items()))
     if op not in ('index','create','update','delete') or metadata.get('_index',parts[0]) not in (parts[0],aliases[parts[0]]):raise ValueError('scope')
     metadata['_index']=aliases[parts[0]];updated.append(json.dumps(action))
     if op!='delete':updated.append(lines[i]);i+=1
    body=('\n'.join(updated)+'\n').encode()
   username=Path(config['usernameFile']).read_text();password=Path(config['passwordFile']).read_text()
   if not username or not password or ':' in username or any(ord(c)<32 for c in username+password):raise ValueError('credentials')
   authorization='Basic '+base64.b64encode((username+':'+password).encode()).decode()
   parts[0]=aliases[parts[0]];target=origin+'/'+('/'.join(parts))+('?' + parsed.query if parsed.query else '')
   request=Request(target,method=self.command,data=body if length else None,headers={'Content-Type':kind,'Authorization':authorization})
   try:
    with opener.open(request,timeout=30) as response:raw=response.read(32*1024*1024+1);status=response.status
   except HTTPError as error:
    status=error.code;error.close();return self.reply(status,b'{"error":"upstream_request_failed"}')
   if len(raw)>32*1024*1024:raise ValueError('response_limit')
   self.reply(status,raw)
  except Exception:self.reply(502,b'{"error":"transport_or_contract_failure"}')
 def reply(self,status,body):
  self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers()
  if self.command!='HEAD':self.wfile.write(body)
 do_GET=do_POST=do_PUT=do_DELETE=do_HEAD=handle_call
ThreadingHTTPServer((config.get('listenAddress','0.0.0.0'),int(config.get('port',9200))),Handler).serve_forever()
