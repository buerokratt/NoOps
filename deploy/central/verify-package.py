#!/usr/bin/env python3
"""Offline integrity and immutable-image checks; no deployment or credentials."""
import ast,hashlib,json,re
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST.json'}
assert actual==set(manifest),'package_file_set_changed'
for name,digest in manifest.items():
 p=root/name;assert p.is_relative_to(root) and '..' not in Path(name).parts
 assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,'package_hash_changed:'+name
 if p.suffix=='.py':ast.parse(p.read_text(),filename=name)
images=json.loads((root/'published-images.json').read_text());assert len(images)==22
assert all(re.fullmatch(r'ghcr.io/[a-z0-9._/-]+@sha256:[a-f0-9]{64}',v) for v in images.values())
assert json.loads((root/'QUALIFICATION.json').read_text())['runtimeDeployment'] is False
print(json.dumps({'status':'PASS','files':len(manifest),'digestBoundImages':len(images),'remoteAcceptance':False}))
