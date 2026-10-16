#!/usr/bin/env python3
"""Build a digest-bound operator artifact from reviewed source locks; never deploy."""
import argparse,hashlib,json,os,re,shutil,subprocess,tarfile,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(args,**kwargs):return subprocess.check_output(args,text=True,**kwargs).strip()
def lock():
 d=json.loads((ROOT/'source-lock.json').read_text());assert len(d['repositories'])==11
 for name,row in d['repositories'].items():
  assert re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',row['repository'])
  assert re.fullmatch('[a-f0-9]{40}',row['commit'])
 components=[c for row in d['repositories'].values() for c in row['components']]
 assert len(components)==15 and len(set(components))==15
 return d
def materialize():
 d=lock();out=ROOT/'sources';out.mkdir(exist_ok=True)
 for name,row in d['repositories'].items():
  target=out/name
  if target.exists():raise ValueError('source_directory_exists_'+name)
  url='https://codeload.github.com/'+row['repository']+'/tar.gz/'+row['commit']
  with urllib.request.urlopen(url,timeout=120) as response:
   with tarfile.open(fileobj=response,mode='r|gz') as archive:
    for member in archive:
     parts=Path(member.name).parts[1:]
     if not parts:continue
     assert '..' not in parts
     if member.isfile():
      p=target.joinpath(*parts);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(archive.extractfile(member).read());p.chmod(member.mode)
 run(['python3',str(ROOT/'deployment/assemble-bundle.py')],cwd=ROOT)
 print(json.dumps({'status':'MATERIALIZED','repositories':len(d['repositories']),'runtimeActions':False}))
def build_release():
 d=lock();repo=os.environ['GITHUB_REPOSITORY'].lower();sha=os.environ['GITHUB_SHA'];assert re.fullmatch('[a-f0-9]{40}',sha)
 out=ROOT/'.central-release';assert not out.exists();out.mkdir();resolved={}
 for name,row in d['repositories'].items():
  for component in row['components']:
   tag='ghcr.io/'+row['repository'].lower()+'/central-'+component.lower()+':sha-'+row['commit']
   run(['docker','pull','--platform','linux/amd64',tag])
   info=json.loads(run(['docker','image','inspect',tag]))[0];labels=info['Config'].get('Labels') or {}
   assert labels.get('org.opencontainers.image.revision')==row['commit'],component
   assert labels.get('org.opencontainers.image.source','').lower()=='https://github.com/'+row['repository'].lower(),component
   digs=[x for x in info.get('RepoDigests',[]) if x.startswith(tag.split(':sha-')[0]+'@sha256:')];assert len(digs)==1,component
   resolved[component]=digs[0]
 def image(key,file,args=()):
  tag='ghcr.io/'+repo+'/central-'+key.lower()+':sha-'+sha;meta=out/(key+'.metadata.json')
  run(['docker','buildx','build','--platform','linux/amd64','--target','runtime','--file',str(file),'--label','org.opencontainers.image.source=https://github.com/'+repo,'--label','org.opencontainers.image.revision='+sha,'--tag',tag,'--push','--metadata-file',str(meta),*args,str(ROOT)])
  digest=json.loads(meta.read_text())['containerimage.digest'];assert re.fullmatch('sha256:[a-f0-9]{64}',digest)
  return tag.split(':sha-')[0]+'@'+digest
 images={key:resolved[key] for key in ['ruuter','resql','tim','cron','datamapper','knowledge','legacy','servicePipeline','llm','llmNotification']}
 args=[]
 for arg,key in [('CHATBOT_IMAGE','backoffice'),('WIDGET_IMAGE','widget'),('SERVICE_IMAGE','service-gui'),('CKB_IMAGE','ckb-gui'),('LLM_IMAGE','llm-gui')]:args+=['--build-arg',arg+'='+resolved[key]]
 images['frontend']=image('frontend',ROOT/'deployment/browser-images/Combined.Dockerfile',args)
 images['dsl']=image('dsl',ROOT/'deployment/package-assets/Dockerfile');images['schemaBase']=images['dsl']
 # Adapter expects its own narrow build context.
 adapter=ROOT/'deployment/opensearch-adapter';file=adapter/'Dockerfile';text=file.read_text().replace('COPY server.py','COPY deployment/opensearch-adapter/server.py').replace(' AS runtime','')
 file=out/'adapter.Dockerfile';file.write_text(text.replace('\nCOPY',' AS runtime\nCOPY',1));images['adapter']=image('adapter',file)
 for key,base in json.loads((ROOT/'public-images.json').read_text()).items():
  file=out/(key+'.Dockerfile');file.write_text('FROM '+base+' AS runtime\n');images[key]=image(key,file)
 assert len(images)==22
 (out/'published-images.json').write_text(json.dumps(images,indent=2)+'\n')
 package=out/'central-operator';package.mkdir()
 for name in ['operator-inventory.py','verify-package.py','README.md','source-lock.json','public-images.json','deployment','runtime']:
  source=ROOT/name;target=package/name
  if source.is_dir():shutil.copytree(source,target,ignore=shutil.ignore_patterns('__pycache__','.git'))
  else:shutil.copy2(source,target)
 for name in ['Service-Module/DSL/OpenSearch/fieldMappings/domain.json','Common-Services/DSL/OpenSearch/fieldMappings/companies.json','Service-Module/DSL/Ruuter/services/GET/slots.yml','LLM-Module/DSL/CronManager/DSL/delete_from_vault.yml']:
  target=package/'sources'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'sources'/name,target)
 shutil.copy2(out/'published-images.json',package/'published-images.json')
 (package/'QUALIFICATION.json').write_text(json.dumps({'status':'CI_BUILT_OPERATOR_ACCEPTANCE_REQUIRED','sourceCommit':sha,'images':22,'modelGeneration':False,'runtimeDeployment':False,'remoteAcceptance':False},indent=2)+'\n')
 entries={str(p.relative_to(package)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(package.rglob('*')) if p.is_file()};(package/'MANIFEST.json').write_text(json.dumps(entries,indent=2)+'\n')
 run(['python3',str(package/'verify-package.py')],cwd=package)
 archive=out/('central-operator-'+sha+'.tar.gz')
 with tarfile.open(archive,'w:gz') as tar:tar.add(package,arcname='central-operator')
 digest=hashlib.file_digest(archive.open('rb'),'sha256').hexdigest();Path(str(archive)+'.sha256').write_text(digest+'  '+archive.name+'\n')
 print(json.dumps({'status':'BUILT_NOT_DEPLOYED','archive':str(archive),'images':len(images)}))
def main():
 p=argparse.ArgumentParser();p.add_argument('action',choices=['validate','materialize','release']);a=p.parse_args()
 if a.action=='validate':d=lock();print(json.dumps({'status':'PASS','repositories':len(d['repositories']),'noClusterAccess':True}))
 elif a.action=='materialize':materialize()
 else:build_release()
if __name__=='__main__':main()
