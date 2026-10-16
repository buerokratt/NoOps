#!/usr/bin/env python3
"""Render a fresh deployment using private create-only state and immutable images."""
import argparse,base64,hashlib,ipaddress,json,os,re,secrets,ssl,subprocess
from pathlib import Path
from urllib.parse import urlsplit
OWNER='central-byk-test';ROOT=Path(__file__).resolve().parents[1]
IMAGE_KEYS=['opensearch','frontend','dsl','ruuter','resql','tim','cron','datamapper','knowledge','legacy','servicePipeline','llm','llmNotification','postgres','redis','qdrant','python','vault','nginx','liquibase','adapter','schemaBase']
class Stop(Exception):pass
def require(value,pattern,label):
 if not isinstance(value,str) or not re.fullmatch(pattern,value):raise Stop('unbound_or_invalid_'+label)
 return value
def origin(value,label,https=True):
 if not isinstance(value,str):raise Stop('unbound_'+label)
 u=urlsplit(value)
 if u.scheme not in (('https',) if https else ('http','https')) or not u.hostname or u.username or u.password or u.path not in ('','/') or u.query or u.fragment:raise Stop('invalid_'+label)
 return value.rstrip('/')
def private_write(path,value):
 if path.exists():
  if path.read_text()==value:return
  raise Stop('create_only_output_conflict')
 path.write_text(value);path.chmod(0o600)
def credentials(state):
 path=state/'credentials.json'
 if path.exists():
  if path.stat().st_mode&0o077:raise Stop('private_state_permissions')
  data=json.loads(path.read_text())
  if data.get('installation')!=OWNER:raise Stop('state_scope_mismatch')
  return data
 password=lambda:'NewTest-A3!'+secrets.token_hex(24)
 data={'installation':OWNER,'accounts':{name:{'username':'admin' if name=='bootstrap' else OWNER+'-'+name,'password':password()} for name in ['bootstrap','chatbot','common','service','knowledge','logging']},'postgresBootstrapPassword':password(),'databasePasswords':{name:password() for name in ['chatbot','service','ckb','llm','tim']},'timKeyPassword':password(),'testUser':{'login':'central-test-'+secrets.token_hex(6),'password':password()}}
 private_write(path,json.dumps(data,indent=2)+'\n');return data
def tls(state):
 if (state/'engine-ca.crt').exists():
  for name in ['engine-ca.key','engine-server.crt','engine-server.key']:assert (state/name).exists()
  return
 commands=[['openssl','req','-x509','-newkey','rsa:3072','-nodes','-sha256','-days','365','-subj','/CN=central-byk-test engine CA','-addext','basicConstraints=critical,CA:TRUE','-addext','keyUsage=critical,keyCertSign,cRLSign','-keyout',str(state/'engine-ca.key'),'-out',str(state/'engine-ca.crt')],['openssl','req','-newkey','rsa:3072','-nodes','-sha256','-subj','/CN=central-byk-test-opensearch.central.svc','-keyout',str(state/'engine-server.key'),'-out',str(state/'engine-server.csr')]]
 for command in commands:subprocess.run(command,check=True,capture_output=True)
 ext=state/'engine-tls.ext';private_write(ext,'subjectAltName=DNS:central-byk-test-opensearch,DNS:central-byk-test-opensearch.central,DNS:central-byk-test-opensearch.central.svc,DNS:central-byk-test-opensearch.central.svc.cluster.local\nextendedKeyUsage=serverAuth\n')
 subprocess.run(['openssl','x509','-req','-in',str(state/'engine-server.csr'),'-CA',str(state/'engine-ca.crt'),'-CAkey',str(state/'engine-ca.key'),'-CAcreateserial','-days','365','-sha256','-extfile',str(ext),'-out',str(state/'engine-server.crt')],check=True,capture_output=True)
 for file in state.glob('engine-*'):file.chmod(0o600)
def render(binding,images,state):
 if binding.get('context')!='rit-byrokratt' or binding.get('applicationNamespace')!=OWNER:raise Stop('target_scope_mismatch')
 for name in ['expectedAPIServer','expectedKubeSystemUID','expectedCentralNamespaceUID','expectedVaultClusterID']:
  if not binding.get(name):raise Stop('unbound_'+name)
 api_port=binding.get('kubernetesAPIPort',443)
 if type(api_port) is not int or not 1<=api_port<=65535:raise Stop('invalid_kubernetes_api_port')
 generation=binding.get('llmGenerationEnabled',False)
 if type(generation) is not bool:raise Stop('invalid_llm_generation_enabled')
 providers=binding.get('llmProviderCIDRs',[])
 if not isinstance(providers,list) or len(providers)>16:raise Stop('invalid_llm_provider_cidrs')
 for value in providers:
  try:network=ipaddress.ip_network(value,strict=True)
  except (TypeError,ValueError):raise Stop('invalid_llm_provider_cidr')
  if network.prefixlen!=network.max_prefixlen or not network.is_global:raise Stop('provider_requires_public_host_cidr')
 if generation and not providers:raise Stop('generation_requires_provider_egress')
 generation_env='true' if generation else 'false'
 access=binding.get('frontendAccessMode','ingress')
 if access not in ('ingress','port-forward'):raise Stop('invalid_frontend_access_mode')
 url=origin(binding.get('frontendOrigin'),'frontendOrigin',access=='ingress');host=urlsplit(url).hostname
 if access=='port-forward' and host not in ('localhost','127.0.0.1','::1'):raise Stop('port_forward_requires_loopback_origin')
 storage=require(binding.get('storageClass'),r'[a-z0-9][a-z0-9.-]*','storageClass')
 ingress=require(binding.get('ingressClass'),r'[a-z0-9][a-z0-9.-]*','ingressClass') if access=='ingress' else None
 vault=origin(binding.get('workloadVaultAddress'),'workloadVaultAddress',not binding.get('allowVaultHTTP',False));origin(binding.get('vaultAddress'),'vaultAddress',not binding.get('allowVaultHTTP',False))
 mount=require(binding.get('vaultKVMount'),r'[A-Za-z0-9_-]+','vaultKVMount');authmount=require(binding.get('vaultAppRoleMount'),r'[A-Za-z0-9_-]+','vaultAppRoleMount')
 if not isinstance(binding.get('vaultPodSelector'),dict) or not binding['vaultPodSelector']:raise Stop('vault_pod_selector_required')
 if access=='ingress' and not binding.get('ingressNamespace'):raise Stop('ingress_namespace_required')
 for name in IMAGE_KEYS:
  require(images.get(name),r'[A-Za-z0-9._:/-]+@sha256:[a-f0-9]{64}','image_'+name)
 pull_name=binding.get('imagePullSecret')
 pull_data=None
 if binding.get('imagePullConfigFile'):
  if pull_name not in (None,OWNER+'-registry-pull'):raise Stop('dedicated_registry_secret_name_required')
  pull_name=OWNER+'-registry-pull';pullfile=Path(binding['imagePullConfigFile'])
  if pullfile.stat().st_mode&0o077:raise Stop('registry_auth_file_must_be_private')
  pull_data=json.loads(pullfile.read_text());hosts={value.split('/')[0] for value in images.values()}
  if set(pull_data)!={'auths'} or set(pull_data['auths'])!=hosts or len(hosts)!=1:raise Stop('only_target_registry_auth_required')
  for entry in pull_data['auths'].values():
   if set(entry)!={'auth'}:raise Stop('inline_registry_auth_required')
   decoded=base64.b64decode(entry['auth'],validate=True).decode()
   if ':' not in decoded or not all(decoded.split(':',1)):raise Stop('invalid_registry_auth')
 c=credentials(state);tls(state);items=[];stages={name:[] for name in ['namespace','storage','provision','schema','vaultDelivery','engineBootstrap','applications','ingress']}
 def resource(api,kind,name,namespace=OWNER,stage='applications',**body):
  value={'apiVersion':api,'kind':kind,'metadata':{'name':name,'labels':{'buerokratt.ee/deployment':OWNER}},**body}
  if namespace:value['metadata']['namespace']=namespace
  value['metadata']['annotations']={'buerokratt.ee/creation-sha256':hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()}
  items.append(value);stages[stage].append({'kind':kind,'name':name,'namespace':namespace});return value
 def secret(name,data,ns=OWNER,stage='storage',annotations=None):
  r=resource('v1','Secret',name,ns,stage=stage,type='Opaque',data={k:base64.b64encode(v.encode() if isinstance(v,str) else v).decode() for k,v in data.items()})
  if annotations:r['metadata']['annotations'].update(annotations)
  return r
 def config(name,data,ns=OWNER,stage='applications'):return resource('v1','ConfigMap',name,ns,stage=stage,data=data)
 def pvc(name,size,ns=OWNER):return resource('v1','PersistentVolumeClaim',name,ns,stage='storage',spec={'accessModes':['ReadWriteOnce'],'storageClassName':storage,'resources':{'requests':{'storage':size}}})
 def env(values):return [{'name':k,'value':str(v)} if not isinstance(v,dict) else {'name':k,'valueFrom':v} for k,v in values.items()]
 def key(name,key):return {'secretKeyRef':{'name':name,'key':key}}
 def volume(name,kind,value):return {'name':name,kind:value}
 def mountv(name,path,ro=False,sub=None):return {'name':name,'mountPath':path,'readOnly':ro,**({'subPath':sub} if sub else {})}
 def container(name,image,values={},mounts=[],command=None,args=None,port=None,memory='128Mi',cpu='100m',readonly=False,probe=None):
  result={'name':name,'image':images[image],'env':env(values),'volumeMounts':mounts,'securityContext':{'allowPrivilegeEscalation':False,'capabilities':{'drop':['ALL']},'readOnlyRootFilesystem':readonly},'resources':{'requests':{'cpu':'25m','memory':'64Mi'},'limits':{'cpu':cpu,'memory':memory}}}
  if command:result['command']=command
  if args:result['args']=args
  if port:result['ports']=[{'name':name[:15],'containerPort':port}]
  if probe:result['readinessProbe']=probe
  return result
 def podspec(containers,volumes=[],inits=[],sa=None):
  r={'automountServiceAccountToken':bool(sa),'securityContext':{'runAsNonRoot':True,'runAsUser':1000,'runAsGroup':1000,'fsGroup':1000,'seccompProfile':{'type':'RuntimeDefault'}},'containers':containers,'volumes':volumes,'initContainers':inits,'nodeSelector':{'kubernetes.io/arch':'amd64'}}
  if sa:r['serviceAccountName']=sa
  if pull_name:r['imagePullSecrets']=[{'name':pull_name}]
  return r
 def deployment(name,containers,volumes=[],inits=[],ns=OWNER):
  labels={'buerokratt.ee/deployment':OWNER,'app':name};resource('apps/v1','Deployment',name,ns,spec={'replicas':1,'strategy':{'type':'Recreate'},'selector':{'matchLabels':labels},'template':{'metadata':{'labels':labels},'spec':podspec(containers,volumes,inits)}})
 def service(name,ports,ns=OWNER,stage='applications'):
  resource('v1','Service',name,ns,stage=stage,spec={'selector':{'buerokratt.ee/deployment':OWNER,'app':name},'ports':[{'name':n,'port':p,'targetPort':p} for n,p in ports]})
 def stateful(name,containers,volumes=[],ns=OWNER):
  labels={'buerokratt.ee/deployment':OWNER,'app':name};resource('apps/v1','StatefulSet',name,ns,stage='storage',spec={'replicas':1,'serviceName':name,'selector':{'matchLabels':labels},'template':{'metadata':{'labels':labels},'spec':podspec(containers,volumes)}})
 def job(name,containers,volumes=[],inits=[],stage='schema',sa=None):
  spec=podspec(containers,volumes,inits,sa);spec['restartPolicy']='Never';resource('batch/v1','Job',name,stage=stage,spec={'backoffLimit':0,'activeDeadlineSeconds':600,'template':{'metadata':{'labels':{'buerokratt.ee/deployment':OWNER,'app':name}},'spec':spec}})
 def copyinit(target='/schemas',image='schemaBase'):
  return container('schema-files',image,mounts=[mountv('schemas',target)],command=['python3','-c'],args=["import shutil;from pathlib import Path;[(shutil.copytree(p,Path('/schemas')/p.name,dirs_exist_ok=True) if p.is_dir() else shutil.copy2(p,Path('/schemas')/p.name)) for p in Path('/bundle/schemas').iterdir()]"],readonly=True)
 resource('v1','Namespace',OWNER,None,stage='namespace')
 if pull_data:
  for namespace in ['central',OWNER]:secret(pull_name,{'.dockerconfigjson':json.dumps(pull_data)},namespace)['type']='kubernetes.io/dockerconfigjson'
 ca=(state/'engine-ca.crt').read_text();secret('engine-tls',{'tls.crt':(state/'engine-server.crt').read_text(),'tls.key':(state/'engine-server.key').read_text()},'central');config('engine-ca',{'ca.crt':ca},'central',stage='storage');config('engine-ca',{'ca.crt':ca},stage='storage')
 secret('engine-admin',c['accounts']['bootstrap'],'central');secret('database-runtime',{'bootstrap-password':c['postgresBootstrapPassword'],**{name+'-password':p for name,p in c['databasePasswords'].items()},'tim-keypass':c['timKeyPassword']})
 secret('initial-test-user',c['testUser']);pvc('application-files','2Gi');pvc('tim-keys','1Gi');pvc('postgres-data','4Gi');pvc('redis-data','1Gi');pvc('qdrant-data','2Gi');pvc('knowledge-data','2Gi');pvc('opensearch-data','10Gi','central')
 nginxmain=(ROOT/'deployment/browser-images/nginx-main.conf').read_text();config('engine-nginx',{'nginx.conf':nginxmain,'default.conf':'server { listen 9443 ssl; ssl_certificate /tls/tls.crt; ssl_certificate_key /tls/tls.key; ssl_protocols TLSv1.2 TLSv1.3; location / { proxy_pass http://127.0.0.1:9200; } }'},'central',stage='storage')
 engine=container('opensearch','opensearch',{'discovery.type':'single-node','cluster.name':OWNER,'OPENSEARCH_INITIAL_ADMIN_PASSWORD':key('engine-admin','password'),'OPENSEARCH_JAVA_OPTS':'-Xms768m -Xmx768m','plugins.security.ssl.http.enabled':'false','node.store.allow_mmap':'false','bootstrap.memory_lock':'false'},[mountv('data','/usr/share/opensearch/data')],memory='2Gi',cpu='1000m',probe={'tcpSocket':{'port':9200},'initialDelaySeconds':30,'periodSeconds':10})
 proxy=container('tls','nginx',mounts=[mountv('tls','/tls',True),mountv('conf','/etc/nginx/nginx.conf',True,'nginx.conf'),mountv('conf','/etc/nginx/conf.d/default.conf',True,'default.conf'),mountv('tmp','/tmp')],command=['nginx','-g','daemon off;'],port=9443,readonly=True)
 stateful(OWNER+'-opensearch',[engine,proxy],[volume('data','persistentVolumeClaim',{'claimName':'opensearch-data'}),volume('tls','secret',{'secretName':'engine-tls','defaultMode':0o440}),volume('conf','configMap',{'name':'engine-nginx'}),volume('tmp','emptyDir',{})],'central');service(OWNER+'-opensearch',[('https',9443)],'central','storage')
 pg=container('postgres','postgres',{'POSTGRES_USER':'byk_bootstrap','POSTGRES_PASSWORD':key('database-runtime','bootstrap-password'),'POSTGRES_DB':'postgres','PGDATA':'/var/lib/postgresql/data/pgdata'},[mountv('data','/var/lib/postgresql/data')],memory='512Mi',cpu='500m',probe={'exec':{'command':['pg_isready','-U','byk_bootstrap','-d','postgres']},'initialDelaySeconds':10,'periodSeconds':5})
 stateful(OWNER+'-postgres',[pg],[volume('data','persistentVolumeClaim',{'claimName':'postgres-data'})]);service(OWNER+'-postgres',[('postgres',5432)],stage='storage')
 # SQL/private credential material stays in a Secret and the private render output.
 sql=[]
 for name,password in c['databasePasswords'].items():
  role='byk_'+name+'_owner';db='byk_'+name
  sql.append("DO $$ BEGIN IF NOT EXISTS(SELECT FROM pg_roles WHERE rolname='%s') THEN CREATE ROLE %s LOGIN PASSWORD '%s' NOSUPERUSER NOCREATEDB NOCREATEROLE; END IF; END $$;"%(role,role,password))
  sql.append("SELECT 'CREATE DATABASE %s OWNER %s' WHERE NOT EXISTS(SELECT FROM pg_database WHERE datname='%s')\n\\gexec"%(db,role,db))
 secret('database-provision',{'provision.sql':'\n'.join(sql)+'\n'})
 pgenv={'PGHOST':OWNER+'-postgres','PGUSER':'byk_bootstrap','PGPASSWORD':key('database-runtime','bootstrap-password'),'PGDATABASE':'postgres'}
 job('database-provision',[container('provision','postgres',pgenv,[mountv('sql','/seed',True)],command=['psql','-v','ON_ERROR_STOP=1','-f','/seed/provision.sql'])],[volume('sql','secret',{'secretName':'database-provision'})],stage='provision')
 for name in ['chatbot','service','ckb','llm','tim']:
  jdbc='jdbc:postgresql://'+OWNER+'-postgres:5432/byk_'+name
  prop='url='+jdbc+'\nusername=byk_'+name+'_owner\npassword='+c['databasePasswords'][name]+'\nchangeLogFile='+('master.xml' if name=='tim' else 'changelog.yaml' if name=='ckb' else 'master.yml')+'\n'
  secret('schema-'+name,{'liquibase.properties':prop},stage='schema')
  lc=container('liquibase','liquibase',{'JAVA_OPTS':'-Xms64m -Xmx256m'},mounts=[mountv('schemas','/schemas',True),mountv('properties','/run/properties',True),mountv('tmp','/tmp')],command=['/liquibase/liquibase','--defaults-file=/run/properties/liquibase.properties','update'],memory='512Mi',cpu='500m');lc['workingDir']='/schemas/'+name;lc['securityContext'].update({'runAsUser':1001,'runAsGroup':1001})
  job('schema-'+name,[lc],[volume('schemas','emptyDir',{}),volume('properties','secret',{'secretName':'schema-'+name}),volume('tmp','emptyDir',{})],[copyinit(image='dsl' if name=='tim' else 'schemaBase')])
 # Create only a new test account; the initializer verifies/reuses it on repetition.
 login=c['testUser']['login'];pwd=c['testUser']['password']
 seed="DO $$ BEGIN IF EXISTS(SELECT FROM \"user\" WHERE login='%s' AND password_hash<>crypt('%s',password_hash)) THEN RAISE EXCEPTION 'test account conflict'; END IF; END $$;\n"%(login,pwd)
 seed+="INSERT INTO \"user\" (login,password_hash,first_name,last_name,id_code,display_name,status,created,csa_title,csa_email) SELECT '%s',crypt('%s',gen_salt('bf',10)),'Central','Tester','%s','Central Test Admin','active',now(),'Agent','test@example.invalid' WHERE NOT EXISTS(SELECT FROM \"user\" WHERE login='%s');\n"%(login,pwd,login,login)
 seed+="INSERT INTO user_authority(user_id,authority_name,created) SELECT '%s',ARRAY['ROLE_ADMINISTRATOR','ROLE_CUSTOMER_SUPPORT_AGENT'],now() WHERE NOT EXISTS(SELECT FROM user_authority WHERE user_id='%s');\n"%(login,login)
 for k,v in {'session_length':'60','away_status_active':'false','is_bot_active':'false','bot_institution_id':'generation-disabled','institution_name':'Fresh Central Test','welcome_message':'Fresh test: connect to an agent.','organizationWorkingAllTime':'true','organizationUseCSA':'true'}.items():seed+="INSERT INTO configuration(key,value,created) SELECT '%s','%s',now() WHERE NOT EXISTS(SELECT FROM configuration WHERE key='central_byk_test_initialized' AND value='1');\n"%(k,v)
 seed+="INSERT INTO configuration(key,value,created) SELECT 'central_byk_test_initialized','1',now() WHERE NOT EXISTS(SELECT FROM configuration WHERE key='central_byk_test_initialized' AND value='1');\n"
 seed='BEGIN;\n'+seed+'COMMIT;\n'
 secret('initial-user-sql',{'seed.sql':seed},stage='schema');job('initial-test-user',[container('seed','postgres',{**pgenv,'PGDATABASE':'byk_chatbot'},[mountv('sql','/seed',True)],command=['psql','-v','ON_ERROR_STOP=1','-f','/seed/seed.sql'])],[volume('sql','secret',{'secretName':'initial-user-sql'})])
 config('tim-key-initializer',{'init.sh':(ROOT/'deployment/tim-image/init-keys.sh').read_text()},stage='schema')
 job('tim-keys-initialize',[container('keys','tim',mounts=[mountv('keys','/keys'),mountv('script','/run/init.sh',True,'init.sh'),mountv('password','/run/keypass',True,'tim-keypass')],command=['sh','/run/init.sh'],memory='128Mi')],[volume('keys','persistentVolumeClaim',{'claimName':'tim-keys'}),volume('script','configMap',{'name':'tim-key-initializer'}),volume('password','secret',{'secretName':'database-runtime'})])
 job('application-files-initialize',[container('files','dsl',mounts=[mountv('data','/data')],readonly=True)],[volume('data','persistentVolumeClaim',{'claimName':'application-files'})])
 # Actual tested credential bridge; one target-scoped ServiceAccount per identity.
 config('vault-sync-code',{'sync.py':(ROOT/'deployment/credential-chart/files/sync.py').read_text()},stage='vaultDelivery')
 if binding.get('vaultCAFile'):secret('vault-ca',{'ca.crt':Path(binding['vaultCAFile']).read_text()},stage='vaultDelivery')
 for identity in c['accounts']:
  target='os-'+identity;role=OWNER+'-os-'+identity+'-delivery';name='vault-deliver-'+identity
  secret(target,{},stage='vaultDelivery',annotations={'opensearch.buerokratt.ee/vault-path':mount+'/opensearch/'+OWNER+'/'+identity})
  resource('v1','ServiceAccount',name,stage='vaultDelivery',automountServiceAccountToken=False)
  resource('rbac.authorization.k8s.io/v1','Role',name,stage='vaultDelivery',rules=[{'apiGroups':[''],'resources':['secrets'],'resourceNames':[target],'verbs':['get','patch']}])
  resource('rbac.authorization.k8s.io/v1','RoleBinding',name,stage='vaultDelivery',subjects=[{'kind':'ServiceAccount','name':name,'namespace':OWNER}],roleRef={'apiGroup':'rbac.authorization.k8s.io','kind':'Role','name':name})
  values={'VAULT_ADDR':vault,'VAULT_APPROLE_MOUNT':authmount,'VAULT_KV_MOUNT':mount,'VAULT_SECRET_PATH':'opensearch/'+OWNER+'/'+identity,'VAULT_ALLOW_INSECURE_HTTP':str(binding.get('allowVaultHTTP',False)).lower(),'TARGET_SECRET':target,'TARGET_NAMESPACE':OWNER}
  volumes=[volume('script','configMap',{'name':'vault-sync-code'}),volume('approle','secret',{'secretName':role+'-approle','defaultMode':0o440})];mounts=[mountv('script','/app',True),mountv('approle','/approle',True)]
  if binding.get('vaultCAFile'):values['VAULT_CACERT']='/vault-ca/ca.crt';volumes.append(volume('vault-ca','secret',{'secretName':'vault-ca'}));mounts.append(mountv('vault-ca','/vault-ca',True))
  job(name,[container('sync','python',values,mounts,command=['python3','-B','/app/sync.py'],readonly=True)],volumes,stage='vaultDelivery',sa=name)
 schemas={OWNER+'-chatbot-notifications':{'properties':{'channelId':{'type':'keyword'},'payload':{'type':'object'},'timestamp':{'type':'keyword'},'sentTo':{'type':'keyword'}}},OWNER+'-chatbot-chatqueue':{'properties':{'chatId':{'type':'keyword'},'timestamp':{'type':'keyword'}}},OWNER+'-service-domain':json.loads((ROOT/'sources/Service-Module/DSL/OpenSearch/fieldMappings/domain.json').read_text())['mappings'],OWNER+'-service-rules':{'properties':{'rule':{'type':'text'}}},OWNER+'-service-services':{'dynamic':True},OWNER+'-logging-ruuterlog':{'dynamic':True},OWNER+'-common-companies':json.loads((ROOT/'sources/Common-Services/DSL/OpenSearch/fieldMappings/companies.json').read_text())['mappings'],OWNER+'-common-municipalities':json.loads((ROOT/'runtime/imports/municipalities-schema.json').read_text())['mappings']}
 config('engine-bootstrap-code',{'bootstrap.py':(ROOT/'deployment/engine-bootstrap.py').read_text(),'indices.json':json.dumps(schemas)},stage='engineBootstrap')
 bootvols=[volume('code','configMap',{'name':'engine-bootstrap-code'}),volume('ca','configMap',{'name':'engine-ca'})];bootmounts=[mountv('code','/config',True),mountv('ca','/engine-ca',True)]
 for identity in c['accounts']:
  bootvols.append(volume(identity,'secret',{'secretName':'os-'+identity,'defaultMode':0o440}));bootmounts.append(mountv(identity,'/run/'+identity,True))
 job('engine-bootstrap',[container('bootstrap','python',{'OPENSEARCH_URL':'https://'+OWNER+'-opensearch.central.svc:9443'},bootmounts,command=['python3','-B','/config/bootstrap.py'],readonly=True)],bootvols,stage='engineBootstrap')
 # Agent config is loopback only. Its upstream Vault address/CA are operator bound.
 def agent(kind,port):
  role=OWNER+'-llm-'+kind;cfg='vault-agent-'+kind
  lines=['pid_file = "/tmp/vault.pid"','vault {', '  address = '+json.dumps(vault)]
  if binding.get('vaultCAFile'):lines.append('  ca_cert = "/vault-ca/ca.crt"')
  lines += ['}', 'auto_auth {', '  method "approle" {', '    mount_path = "auth/'+authmount+'"', '    config = { role_id_file_path = "/approle/role_id", secret_id_file_path = "/approle/secret_id", remove_secret_id_file_after_reading = false }', '  }', '  sink "file" { config = { path = "/tmp/token" } }', '}', 'listener "tcp" {', '  address = "127.0.0.1:'+str(port)+'"', '  tls_disable = true', '}', 'api_proxy { use_auto_auth_token = "force" }']

  config(cfg,{'agent.hcl':'\n'.join(lines)+'\n'});vs=[volume(cfg+'-conf','configMap',{'name':cfg}),volume(cfg+'-role','secret',{'secretName':role+'-approle','defaultMode':0o440}),volume(cfg+'-tmp','emptyDir',{})];ms=[mountv(cfg+'-conf','/config',True),mountv(cfg+'-role','/approle',True),mountv(cfg+'-tmp','/tmp')]
  if binding.get('vaultCAFile'):vs.append(volume('vault-ca','secret',{'secretName':'vault-ca'}));ms.append(mountv('vault-ca','/vault-ca',True))
  return container(cfg,'vault',mounts=ms,command=['vault','agent','-config=/config/agent.hcl'],readonly=True),vs
 # Bound in-namespace HTTP dependencies; Central OpenSearch transport is verified TLS.
 ini=(ROOT/'runtime/full/constants.ini').read_text()
 replacements={'CHATBOT_TIM':'http://127.0.0.1:8085','SERVICE_TIM':'http://127.0.0.1:8085','RAG_SEARCH_TIM':'http://127.0.0.1:8085','CHATBOT_RESQL':'http://127.0.0.1:8082/backoffice','SERVICE_RESQL':'http://127.0.0.1:8082/services','CKB_USERS_RESQL':'http://127.0.0.1:8082/users','CKB_RESQL':'http://127.0.0.1:8082/ckb','RAG_SEARCH_RESQL':'http://127.0.0.1:8082/rag-search','CHATBOT_RUUTER_PRIVATE':'http://127.0.0.1:8088/backoffice','CHATBOT_RUUTER_PUBLIC':'http://127.0.0.1:8086/backoffice','CHATBOT_RUUTER_PRIVATE_INTERNAL':'http://127.0.0.1:8088/backoffice','CHATBOT_RUUTER_PUBLIC_INTERNAL':'http://127.0.0.1:8086/backoffice','CHATBOT_DMAPPER':'http://127.0.0.1:3000','CHATBOT_DMAPPER_HBS':'http://127.0.0.1:3000/hbs/backoffice','DMAPPER':'http://127.0.0.1:3000','SERVICE_DMAPPER':'http://127.0.0.1:3000','SERVICE_DMAPPER_HBS':'http://127.0.0.1:3000/hbs/services','CKB_DMAPPER':'http://127.0.0.1:3000','CKB_DMAPPER_HBS':'http://127.0.0.1:3000/hbs/ckb','RAG_SEARCH_DMAPPER':'http://127.0.0.1:3000','CHATBOT_OPENSEARCH':'http://127.0.0.1:9401','OPENSEARCH':'http://127.0.0.1:9402','SERVICE_OPENSEARCH':'http://127.0.0.1:9403','CHATBOT_NOTIFICATIONS':'http://'+OWNER+'-notification:4040','CKB_SEARCH':'http://'+OWNER+'-knowledge:3000','CKB_SEARCH_SERVICE':'http://'+OWNER+'-knowledge:3000','CHATBOT_CRON_MANAGER':'http://127.0.0.1:9010','RAG_SEARCH_CRON_MANAGER':'http://127.0.0.1:9010','CRON_MANAGER':'http://127.0.0.1:9010','VAULT_AGENT_URL':'http://127.0.0.1:8203','VAULT_AGENT_BACKOFFICE':'http://127.0.0.1:8203','SERVICES_PIPELINE':'http://127.0.0.1:3010','DOMAIN':host,'SERVICE_OPENAPI_ALLOWED_ORIGINS':','.join(binding.get('serviceOpenAPIAllowedOrigins',[])),'RAG_SEARCH_LLM_ORCHESTRATOR':'http://'+OWNER+'-llm:8100/orchestrate','LLM_ORCHESTRATOR_URL':'http://'+OWNER+'-llm:8100'}
 replacements.update({'CKB_TIM':'http://127.0.0.1:8085','CKB_RUUTER':'http://127.0.0.1:8088/ckb','CKB_RUUTER_INTERNAL':'http://127.0.0.1:8088/ckb','SERVICE_RUUTER':'http://127.0.0.1:8088/services','RAG_SEARCH_RUUTER_PUBLIC':'http://127.0.0.1:8086/rag-search','RAG_SEARCH_RUUTER_PRIVATE':'http://127.0.0.1:8088/rag-search','RAG_SEARCH_RUUTER_PUBLIC_INTERNAL_SERVICE':'http://127.0.0.1:8088/services','RAG_SEARCH_LLM_SERVICE':'http://'+OWNER+'-llm:8100','RAG_SEARCH_LLM_CACHE_CLEAR':'http://'+OWNER+'-llm:8100/cache/clear','RAG_SEARCH_PROMPT_REFRESH':'http://'+OWNER+'-llm:8100/prompt-config/refresh','VAULT_PATH_PREFIX':OWNER+'/llm-module','VAULT_KV_MOUNT':mount})
 ini=re.sub(r'^DB_PASSWORD\s*=.*$','',ini,flags=re.M)
 for name,value in replacements.items():
  if re.search(r'^'+re.escape(name)+r'\s*=',ini,re.M):ini=re.sub(r'^'+re.escape(name)+r'\s*=.*$',name+'='+value,ini,flags=re.M)
  else:ini+='\n'+name+'='+value
 config('backend-config',{'constants.ini':ini})
 config('service-empty-state',{'slots.yml':(ROOT/'sources/Service-Module/DSL/Ruuter/services/GET/slots.yml').read_text()})
 config('cron-job-definitions',{name:(ROOT/'deployment/bundle/cron'/name).read_text() for name in ['import_companies_data.yml','import_municipalities_data.yml','store_in_vault.yml']} | {'delete_from_vault.yml':(ROOT/'sources/LLM-Module/DSL/CronManager/DSL/delete_from_vault.yml').read_text()})
 backendvols=[volume('files','persistentVolumeClaim',{'claimName':'application-files'}),volume('config','configMap',{'name':'backend-config'}),volume('keys','persistentVolumeClaim',{'claimName':'tim-keys'}),volume('engine-ca','configMap',{'name':'engine-ca'}),volume('service-empty-state','configMap',{'name':'service-empty-state'}),volume('cron-jobs','configMap',{'name':'cron-job-definitions'})];backend=[]
 for kind,port in [('public',8086),('private',8088),('resql',8082)]:
  values={'SERVER_PORT':port,'JAVA_TOOL_OPTIONS':'-Xmx256m','application.config-path':'/DSL','application.internalRequests.disabled':'true','application.cors.allowedOrigins':url,'application.logging.displayRequestContent':'false','application.logging.displayResponseContent':'false','application.logging.printStackTrace':'false','application.httpCodesAllowList':'200,201,202,204,207,400,401,403,404,409,420,500,503','application.openSearchConfiguration.url':'http://127.0.0.1:9404','application.openSearchConfiguration.index':'ruuterlog'}
  backend.append(container('ruuter-'+kind,'ruuter',values,[mountv('files','/DSL',True,kind),*([mountv('files','/DSL/services',True,'Ruuter/services'),mountv('service-empty-state','/DSL/services/GET/slots.yml',True,'slots.yml')] if kind=='private' else []),mountv('config','/app/constants.ini',True,'constants.ini')],port=port,memory='512Mi',cpu='500m',probe={'tcpSocket':{'port':port},'initialDelaySeconds':10,'periodSeconds':5}))
 resql={'SQLMS_PROJECT_DATASOURCES':'true','sqlms.saved-queries-dir':'/DSL','JAVA_TOOL_OPTIONS':'-Xmx256m'}
 for i,(project,name) in enumerate([('backoffice','chatbot'),('services','service'),('ckb','ckb'),('ragsearch','llm')]):
  for suffix,value in {'NAME':project,'JDBCURL':'jdbc:postgresql://'+OWNER+'-postgres:5432/byk_'+name,'USERNAME':'byk_'+name+'_owner','PASSWORD':key('database-runtime',name+'-password'),'DRIVERCLASSNAME':'org.postgresql.Driver'}.items():resql['SQLMS_DATASOURCES_'+str(i)+'_'+suffix]=value
 backend.append(container('resql','resql',resql,[mountv('files','/DSL',True,'resql')],memory='512Mi',cpu='500m'))
 backend.append(container('tim','tim',{'SPRING_DATASOURCE_URL':'jdbc:postgresql://'+OWNER+'-postgres:5432/byk_tim','SPRING_DATASOURCE_USERNAME':'byk_tim_owner','SPRING_DATASOURCE_PASSWORD':key('database-runtime','tim-password'),'SPRING_LIQUIBASE_ENABLED':'false','JWT_INTEGRATION_SIGNATURE_KEY_STORE':'file:/keys/jwtkeystore.jks','JWT_INTEGRATION_SIGNATURE_KEY_STORE_PASSWORD':key('database-runtime','tim-keypass'),'JWT_INTEGRATION_SIGNATURE_ISSUER':host,'SECURITY_ALLOWLIST_JWT':'127.0.0.1,::1','SERVER_SSL_ENABLED':'false','JAVA_TOOL_OPTIONS':'-Xmx192m'},[mountv('keys','/keys',True)],memory='384Mi',cpu='500m'))
 mappermounts=[mountv('files','/data')]
 # Preserve the tested mount order across extraction/filesystems.
 mapper_order=['services','common-services','rag-search','backoffice','ckb']
 def mapper_sort(path):return (mapper_order.index(path.name) if path.name in mapper_order else len(mapper_order),path.name)
 for directory in sorted((ROOT/'deployment/bundle/mapper/hbs').iterdir(),key=mapper_sort):
  if directory.is_dir():mappermounts.append(mountv('files','/workspace/app/views/'+directory.name,True,'mapper/hbs/'+directory.name))
 for directory in sorted((ROOT/'deployment/bundle/mapper/js').iterdir(),key=mapper_sort):
  if directory.is_dir():mappermounts.append(mountv('files','/workspace/app/js/'+directory.name,True,'mapper/js/'+directory.name))
 mappermounts.append(mountv('files','/workspace/app/module/common-services/hbs',True,'mapper/hbs/common-services'))
 backend.append(container('mapper','datamapper',{'PORT':'3000','CONTENT_FOLDER':'/data'},mappermounts,memory='384Mi',cpu='500m'))
 cron={'SERVER_PORT':'9010','JAVA_TOOL_OPTIONS':'-Xmx192m','application.config-path':'/DSL','CENTRAL_OPENSEARCH_URL':'https://'+OWNER+'-opensearch.central.svc:9443','CENTRAL_DATA_MAPPER_URL':'http://127.0.0.1:3000','CENTRAL_INDEX_PREFIX':OWNER+'-common-','CENTRAL_IMPORT_ALLOW_HTTP':'true','CENTRAL_OS_USERNAME_FILE':'/run/os/username','CENTRAL_OS_PASSWORD_FILE':'/run/os/password','CENTRAL_OS_CA_FILE':'/engine-ca/ca.crt','CENTRAL_IMPORT_ROOT':'/data/OpenSearch/services','CENTRAL_IMPORT_JOURNAL':'/data/import-journal','CENTRAL_MAPPER_IMPORT_ROOT':'/OpenSearch/services','VAULT_PATH_PREFIX':OWNER+'/llm-module','VAULT_KV_MOUNT':mount,'VAULT_ADDR':'http://127.0.0.1:8203','PYTHONPATH':'/app'}
 backendvols.append(volume('os-common','secret',{'secretName':'os-common','defaultMode':0o440}));backend.append(container('cron','cron',cron,[mountv('files','/data'),mountv('cron-jobs','/DSL',True),mountv('config','/app/config/constants.ini',True,'constants.ini'),mountv('os-common','/run/os',True),mountv('engine-ca','/engine-ca',True)],memory='384Mi',cpu='500m'))
 for name,port,aliases,template in [('chatbot',9401,{'notifications':OWNER+'-chatbot-notifications','chatqueue':OWNER+'-chatbot-chatqueue'},None),('common',9402,{'companies':OWNER+'-common-companies','municipalities':OWNER+'-common-municipalities'},'common'),('service',9403,{'domain':OWNER+'-service-domain','rules':OWNER+'-service-rules','services':OWNER+'-service-services','ruuterlog':OWNER+'-logging-ruuterlog'},'service'),('logging',9404,{'ruuterlog':OWNER+'-logging-ruuterlog'},None)]:
  cfg={'origin':'https://'+OWNER+'-opensearch.central.svc:9443','aliases':aliases,'usernameFile':'/run/os/username','passwordFile':'/run/os/password','caFile':'/engine-ca/ca.crt','listenAddress':'127.0.0.1','port':port,'metadataLogging':name=='logging','templateDirectories':['/templates'] if template else []};config('adapter-'+name,{'adapter.json':json.dumps(cfg)})
  backendvols.extend([volume('adapter-'+name,'configMap',{'name':'adapter-'+name})])
  if name!='common':backendvols.append(volume('os-'+name,'secret',{'secretName':'os-'+name,'defaultMode':0o440}))
  ms=[mountv('adapter-'+name,'/config',True),mountv('os-'+name,'/run/os',True),mountv('engine-ca','/engine-ca',True)]
  if template:ms.append(mountv('files','/templates',True,'templates/'+template))
  # The adapter image is bound separately because it contains reviewed source.
  backend.append(container('adapter-'+name,'adapter',{'ADAPTER_CONFIG':'/config/adapter.json'},ms,readonly=True))
 backend.append(container('service-pipeline','servicePipeline',{'PORT':'3010','OPENSEARCH_URL':'https://'+OWNER+'-opensearch.central.svc:9443','OPENSEARCH_INDEX_PREFIX':OWNER+'-service-','OPENSEARCH_USERNAME_FILE':'/run/os/username','OPENSEARCH_PASSWORD_FILE':'/run/os/password','OPENSEARCH_CA_FILE':'/engine-ca/ca.crt'},[mountv('os-service','/run/os',True),mountv('engine-ca','/engine-ca',True)],memory='256Mi',cpu='200m'))
 a,vs=agent('cron',8203);backend.append(a);backendvols+=vs
 deployment(OWNER+'-backend',backend,backendvols);service(OWNER+'-backend',[('public',8086),('private',8088),('resql',8082)])
 for name,image,port,size,command,values in [('redis','redis',6379,'1Gi',['redis-server','--appendonly','yes'],{}),('qdrant','qdrant',6333,'2Gi',None,{'QDRANT__STORAGE__SNAPSHOTS_PATH':'/qdrant/storage/snapshots'})]:
  path='/data' if name=='redis' else '/qdrant/storage';co=container(name,image,values,[mountv('data',path)],command=command,port=port,memory='512Mi',cpu='500m',probe=({'exec':{'command':['redis-cli','ping']},'initialDelaySeconds':5,'periodSeconds':5} if name=='redis' else {'httpGet':{'path':'/readyz','port':6333},'initialDelaySeconds':10,'periodSeconds':5}));stateful(OWNER+'-'+name,[co],[volume('data','persistentVolumeClaim',{'claimName':name+'-data'})]);service(OWNER+'-'+name,[(name,port)],stage='storage')
 note=container('notification','legacy',{'PORT':'4040','CORS_WHITELIST_ORIGINS':url,'LLM_GENERATION_ENABLED':generation_env,'OPENSEARCH_URL':'https://'+OWNER+'-opensearch.central.svc:9443','OPENSEARCH_INDEX_PREFIX':OWNER+'-chatbot-','OPENSEARCH_USERNAME_FILE':'/run/os/username','OPENSEARCH_PASSWORD_FILE':'/run/os/password','OPENSEARCH_CA_FILE':'/engine-ca/ca.crt','PRIVATE_RUUTER_URL':'http://'+OWNER+'-backend:8088','PUBLIC_RUUTER_URL':'http://'+OWNER+'-backend:8086','RUUTER_URL':'http://'+OWNER+'-backend:8086','LLM_ORCHESTRATOR_URL':'http://'+OWNER+'-llm:8100'},[mountv('auth','/run/os',True),mountv('ca','/engine-ca',True)],port=4040,memory='384Mi',cpu='500m')
 deployment(OWNER+'-notification',[note],[volume('auth','secret',{'secretName':'os-chatbot','defaultMode':0o440}),volume('ca','configMap',{'name':'engine-ca'})]);service(OWNER+'-notification',[('http',4040)])
 knowledge=container('knowledge','knowledge',{'PORT':'3000','OPENSEARCH_URL':'https://'+OWNER+'-opensearch.central.svc:9443','OPENSEARCH_INDEX_PREFIX':OWNER+'-knowledge-','OPENSEARCH_USERNAME_FILE':'/run/os/username','OPENSEARCH_PASSWORD_FILE':'/run/os/password','OPENSEARCH_CA_FILE':'/engine-ca/ca.crt'},[mountv('auth','/run/os',True),mountv('ca','/engine-ca',True),mountv('data','/app/data')],port=3000,memory='256Mi',cpu='500m')
 deployment(OWNER+'-knowledge',[knowledge],[volume('auth','secret',{'secretName':'os-knowledge','defaultMode':0o440}),volume('ca','configMap',{'name':'engine-ca'}),volume('data','persistentVolumeClaim',{'claimName':'knowledge-data'})]);service(OWNER+'-knowledge',[('http',3000)])
 a,vs=agent('llm',8201);config('llm-config',{'constants.ini':'[DSL]\nLOKI_URL=\n'+''.join(k+'='+v+'\n' for k,v in {'RAG_SEARCH_RESQL':'http://'+OWNER+'-backend:8082/rag-search','RAG_SEARCH_RUUTER_PUBLIC':'http://'+OWNER+'-backend:8086/rag-search','RAG_SEARCH_RUUTER_PRIVATE':'http://'+OWNER+'-backend:8088/rag-search','RAG_SEARCH_RUUTER_PUBLIC_INTERNAL_SERVICE':'http://'+OWNER+'-backend:8088/services','RUUTER_COMMON_SERVICE_BASE_URL':'http://'+OWNER+'-backend:8086/common-services','RAG_SEARCH_LLM_SERVICE':'http://127.0.0.1:8100','QDRANT_URL':'http://'+OWNER+'-qdrant:6333','LANGFUSE_URL':'http://127.0.0.1:3000'}.items())});llm=container('llm','llm',{'LLM_GENERATION_ENABLED':generation_env,'REDIS_HOST':OWNER+'-redis','QDRANT_URL':'http://'+OWNER+'-qdrant:6333','RAG_SEARCH_CONSTANTS':'/config/constants.ini','VAULT_ADDR':'http://127.0.0.1:8201','VAULT_USE_TOKEN_FILE':'false','VAULT_PATH_PREFIX':OWNER+'/llm-module','VAULT_KV_MOUNT':mount,'HF_HUB_OFFLINE':'1','TRANSFORMERS_OFFLINE':'1','HF_HOME':'/tmp/no-models','GUARDRAILS_EMBEDDING_PATH':'/opt/guardrails-embeddings','FASTEMBED_CACHE_PATH':'/tmp/fastembed_cache'},[mountv('config','/config',True)],port=8100,memory='3Gi',cpu='1000m',probe={'httpGet':{'path':'/health','port':8100},'initialDelaySeconds':30,'periodSeconds':10});relay=container('llm-relay','llmNotification',{'LLM_ORCHESTRATOR_URL':'http://127.0.0.1:8100','CORS_WHITELIST_ORIGINS':url},port=4040,memory='128Mi')
 deployment(OWNER+'-llm',[llm,relay,a],[volume('config','configMap',{'name':'llm-config'}),*vs]);service(OWNER+'-llm',[('api',8100),('sse',4040)])
 frontconf='server { listen 8080; server_tokens off; root /usr/share/nginx/html; location = / { return 302 /chat/; } location = /chat/auth { try_files /login.html =404; } location /chat/ { try_files $uri $uri/ /chat/index.html; } location /widget/ { try_files $uri $uri/ /widget/index.html; } location /services/ { try_files $uri $uri/ /services/index.html; } location /ckb/ { try_files $uri $uri/ /ckb/index.html; } location /rag-search/ { try_files $uri $uri/ /rag-search/index.html; } location /api/public/ { proxy_pass http://'+OWNER+'-backend:8086/; proxy_set_header Host $host; } location /api/private/ { proxy_pass http://'+OWNER+'-backend:8088/; proxy_set_header Host $host; } location /notifications/ { proxy_pass http://'+OWNER+'-notification:4040/; proxy_buffering off; proxy_read_timeout 3600s; } location /llm-notifications/ { proxy_pass http://'+OWNER+'-llm:4040/; proxy_buffering off; proxy_read_timeout 3600s; } location ~ ^/vault-agent-gui/v1/'+mount+'/data/'+OWNER+'/llm-module/encryption/public_key$ { limit_except GET { deny all; } rewrite ^/vault-agent-gui/(.*)$ /$1 break; proxy_pass http://127.0.0.1:8202; } location /vault-agent-gui/ { return 404; } location /status { return 200 "alive"; } }'
 config('frontend-config',{'default.conf':frontconf,'runtime-config.js':'window.centralVault='+json.dumps({'prefix':OWNER+'/llm-module','mount':mount})+';'});a,vs=agent('gui',8202);front=container('frontend','frontend',mounts=[mountv('config','/etc/nginx/conf.d/default.conf',True,'default.conf'),mountv('config','/usr/share/nginx/html/runtime-config.js',True,'runtime-config.js'),mountv('tmp','/tmp')],port=8080,readonly=True,probe={'httpGet':{'path':'/status','port':8080},'initialDelaySeconds':5,'periodSeconds':5})
 deployment(OWNER+'-frontend',[front,a],[volume('config','configMap',{'name':'frontend-config'}),volume('tmp','emptyDir',{}),*vs]);service(OWNER+'-frontend',[('http',8080)])
 if access=='ingress':
  certfile=Path(binding.get('frontendTLSCertFile') or '');keyfile=Path(binding.get('frontendTLSKeyFile') or '')
  if not certfile.is_file() or not keyfile.is_file():raise Stop('dedicated_frontend_tls_files_required')
  if keyfile.stat().st_mode&0o077:raise Stop('frontend_tls_key_must_be_private')
  subprocess.run(['openssl','x509','-in',str(certfile),'-noout','-checkhost',host],check=True,capture_output=True)
  subprocess.run(['openssl','x509','-in',str(certfile),'-noout','-checkend','3600'],check=True,capture_output=True)
  certpub=subprocess.run(['openssl','x509','-in',str(certfile),'-noout','-pubkey'],check=True,capture_output=True).stdout
  keypub=subprocess.run(['openssl','pkey','-in',str(keyfile),'-pubout'],check=True,capture_output=True).stdout
  if certpub!=keypub:raise Stop('frontend_tls_key_pair_mismatch')
  tlssecret=secret('frontend-tls',{'tls.crt':certfile.read_text(),'tls.key':keyfile.read_text()},stage='ingress');tlssecret['type']='kubernetes.io/tls'
  resource('networking.k8s.io/v1','Ingress',OWNER,stage='ingress',spec={'ingressClassName':ingress,'tls':[{'hosts':[host],'secretName':'frontend-tls'}],'rules':[{'host':host,'http':{'paths':[{'path':'/','pathType':'Prefix','backend':{'service':{'name':OWNER+'-frontend','port':{'number':8080}}}}]}}]})
 # New test namespace only: no API credentials in normal workloads and no shared ingress.
 frontend_ingress=[{'from':[{'podSelector':{}}]}]
 if access=='ingress':frontend_ingress.append({'from':[{'namespaceSelector':{'matchLabels':{'kubernetes.io/metadata.name':binding['ingressNamespace']}}}],'ports':[{'protocol':'TCP','port':8080}]})
 resource('networking.k8s.io/v1','NetworkPolicy','test-isolation',spec={'podSelector':{},'policyTypes':['Ingress','Egress'],'ingress':frontend_ingress,'egress':[{'to':[{'podSelector':{}}]},{'to':[{'namespaceSelector':{'matchLabels':{'kubernetes.io/metadata.name':'kube-system'}}}],'ports':[{'protocol':'UDP','port':53},{'protocol':'TCP','port':53}]},{'to':[{'namespaceSelector':{'matchLabels':{'kubernetes.io/metadata.name':'central'}},'podSelector':{'matchLabels':{'buerokratt.ee/deployment':OWNER}}}],'ports':[{'protocol':'TCP','port':9443}]},{'to':[{'namespaceSelector':{'matchLabels':{'kubernetes.io/metadata.name':'central'}},'podSelector':{'matchLabels':binding['vaultPodSelector']}}],'ports':[{'protocol':'TCP','port':int(binding.get('vaultPort',8200))}]}]})
 # Delivery jobs alone reach the Kubernetes API. Bind the destination IP/port
 # seen by the CNI after service DNAT (often an API endpoint on TCP6443).
 if generation:
  resource('networking.k8s.io/v1','NetworkPolicy','llm-provider-egress',spec={'podSelector':{'matchLabels':{'app':OWNER+'-llm'}},'policyTypes':['Egress'],'egress':[{'to':[{'ipBlock':{'cidr':value}} for value in providers],'ports':[{'protocol':'TCP','port':443}]}]})
 cidr=str(ipaddress.ip_network(binding.get('kubernetesAPICIDR',''),strict=False));resource('networking.k8s.io/v1','NetworkPolicy','vault-delivery-api',spec={'podSelector':{'matchExpressions':[{'key':'app','operator':'In','values':['vault-deliver-'+x for x in c['accounts']]}]},'policyTypes':['Egress'],'egress':[{'to':[{'ipBlock':{'cidr':cidr}}],'ports':[{'protocol':'TCP','port':api_port}]}]})
 resource('networking.k8s.io/v1','NetworkPolicy','engine-isolation','central',spec={'podSelector':{'matchLabels':{'buerokratt.ee/deployment':OWNER}},'policyTypes':['Ingress'],'ingress':[{'from':[{'namespaceSelector':{'matchLabels':{'kubernetes.io/metadata.name':OWNER}}}],'ports':[{'protocol':'TCP','port':9443}]}]})
 for item in items:
  copied=json.loads(json.dumps(item));copied['metadata']['annotations'].pop('buerokratt.ee/creation-sha256',None)
  item['metadata']['annotations']['buerokratt.ee/creation-sha256']=hashlib.sha256(json.dumps(copied,sort_keys=True).encode()).hexdigest()
 return {'apiVersion':'v1','kind':'List','items':items},stages,c
if __name__=='__main__':
 try:
  p=argparse.ArgumentParser();p.add_argument('--bindings',required=True);p.add_argument('--images',required=True);p.add_argument('--state-dir',required=True);p.add_argument('--output',required=True);a=p.parse_args()
  state=Path(a.state_dir);state.mkdir(mode=0o700,parents=True,exist_ok=True)
  if state.stat().st_mode&0o077:raise Stop('state_directory_must_be_private')
  os.umask(0o077);binding=json.loads(Path(a.bindings).read_text());images=json.loads(Path(a.images).read_text());require(images.get('adapter'),r'[A-Za-z0-9._:/-]+@sha256:[a-f0-9]{64}','image_adapter')
  manifest,stages,c=render(binding,images,state);output=Path(a.output);private_write(output,json.dumps(manifest,indent=2)+'\n');private_write(state/'stages.json',json.dumps(stages,indent=2)+'\n');private_write(state/'opensearch-accounts.json',json.dumps({'installation':OWNER,'accounts':c['accounts']},indent=2)+'\n')
  print(json.dumps({'status':'RENDERED','resources':len(manifest['items']),'context':'rit-byrokratt','namespace':OWNER,'privateOutput':str(output),'noRemoteExecution':True}))
 except Stop as e:print('Stopped:',str(e));raise SystemExit(1)
