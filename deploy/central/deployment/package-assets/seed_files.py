"""Create-only namespace-owned DSL seed; preserve all later runtime edits."""
import hashlib,json,os,shutil
from pathlib import Path
source=Path('/bundle');target=Path('/data');fingerprint=(source/'BUNDLE-SHA256').read_text().strip();marker=target/'.central-byk-test-initialized'
if marker.exists():
 if marker.read_text().strip()!=fingerprint:raise SystemExit('Existing DSL bundle differs; refuse implicit upgrade/reseed')
 print('Existing task DSL state retained');raise SystemExit(0)
if any(path.name != 'lost+found' or not path.is_dir() or any(path.iterdir()) for path in target.iterdir()):raise SystemExit('Refuse seeding nonempty unknown application storage')
for name in ['private','public','resql','mapper','cron','templates']:
 shutil.copytree(source/name,target/name)
for name in ['OpenSearch/services/companies/unprocessed','OpenSearch/services/companies/processed','OpenSearch/services/municipalities/unprocessed','OpenSearch/services/municipalities/processed','import-journal','knowledge','Ruuter/services','DMAPPER/services']:(target/name).mkdir(parents=True,exist_ok=True)
# The Service file API gets a dedicated subtree, not unrelated module files.
shutil.copytree(target/'private/services',target/'Ruuter/services',dirs_exist_ok=True)
with marker.open('x') as file:file.write(fingerprint+'\n');file.flush();os.fsync(file.fileno())
print('New task-owned DSL/import storage initialized once')
