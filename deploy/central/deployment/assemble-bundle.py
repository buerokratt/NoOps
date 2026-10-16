"""Assemble pinned module files with explicit collision checks; no runtime data."""
from pathlib import Path
import hashlib,json,shutil
root=Path(__file__).resolve().parents[1];out=root/'deployment/bundle'
if out.exists():shutil.rmtree(out)
out.mkdir();owners={}
def copy(source,target):
 for file in sorted((root/source).rglob('*')):
  if not file.is_file() or file.suffix in ('.md','.txt','.sh','.html','.csv') and target.startswith(('private','public')):continue
  relative=Path(target)/file.relative_to(root/source);key=str(relative);data=file.read_bytes();dest=out/relative
  if dest.exists() and dest.read_bytes()!=data:raise RuntimeError('DSL collision: '+key+' '+str(file))
  dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);owners[key]=str(file.relative_to(root))
for repo in ['Buerokratt-Chatbot','Common-Knowledge','LLM-Module']:
 for kind in ['private','public']:
  source='sources/'+repo+'/DSL/Ruuter.'+kind
  if (root/source).exists():copy(source,kind)
copy('sources/Service-Module/DSL/Ruuter','private');copy('sources/Common-Knowledge/DSL/Ruuter','private');copy('sources/Common-Services/DSL/Ruuter.public','public/common-services')
for repo in ['Buerokratt-Chatbot','Service-Module','Common-Knowledge','LLM-Module']:
 copy('sources/'+repo+'/DSL/Resql','resql')
 mapper=root/'sources'/repo/'DSL/DMapper'
 if mapper.exists():
  for project in mapper.iterdir():
   if project.is_dir():
    for kind in ['hbs','js']:
     if (project/kind).exists():copy(str((project/kind).relative_to(root)),'mapper/'+kind+'/'+project.name)
copy('sources/Common-Services/DSL/DMapper/hbs','mapper/hbs/common-services')
for filename in ['import_companies_data.yml','import_municipalities_data.yml']:
 file=root/'sources/Common-Services/DSL/CronManager'/filename;dest=out/'cron'/filename;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(file.read_bytes());owners[str(dest.relative_to(out))]=str(file.relative_to(root))
for filename in ['store_in_vault.yml','delete_from_vault.yml']:
 file=root/'sources/LLM-Module/DSL/CronManager/DSL'/filename
 if file.exists():dest=out/'cron'/filename;dest.write_bytes(file.read_bytes());owners[str(dest.relative_to(out))]=str(file.relative_to(root))
for repo,key in [('Buerokratt-Chatbot','chatbot'),('Service-Module','service'),('Common-Knowledge','ckb'),('LLM-Module','llm')]:copy('sources/'+repo+'/DSL/Liquibase','schemas/'+key)
copy('sources/TIM/src/main/resources/changelog','schemas/tim/changelog')
copy('sources/TIM/src/main/resources/data','schemas/tim/data')
for filename in ['master.xml','schema-postgre.sql']:
 file=root/'sources/TIM/src/main/resources'/filename;dest=out/'schemas/tim'/filename;dest.write_bytes(file.read_bytes());owners[str(dest.relative_to(out))]=str(file.relative_to(root))
for repo,key in [('Common-Services','common'),('Service-Module','service')]:copy('sources/'+repo+'/DSL/OpenSearch/templates','templates/'+key)
for name in ['private','public','resql','mapper/hbs','mapper/js','cron','templates']:(out/name).mkdir(parents=True,exist_ok=True)
entries=[{'path':str(p.relative_to(out)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source':owners[str(p.relative_to(out))]} for p in sorted(out.rglob('*')) if p.is_file()]
fingerprint=hashlib.sha256(json.dumps(entries,sort_keys=True).encode()).hexdigest();(out/'BUNDLE-SHA256').write_text(fingerprint+'\n');(root/'deployment/bundle-manifest.json').write_text(json.dumps({'sha256':fingerprint,'files':entries,'SQLSchemaRewrites':False,'runtimeStateCopied':False},indent=2)+'\n')
print(json.dumps({'files':len(entries),'bundleSHA256':fingerprint,'runtimeStateCopied':False}))
