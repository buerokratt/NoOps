"""Preload health must prove the requested environment, not an arbitrary adapter."""
import importlib.util,json
from pathlib import Path
s=importlib.util.spec_from_file_location('guardrails_health',Path(__file__).resolve().parents[1]/'deployment/guardrails-health.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
health={'generation_enabled':True,'guardrails_embedding_loaded':True,'guardrails_loaded':True,'guardrails_environments':['testing'],'redis_session_store':'connected'}
assert m.ready(health,'testing') and not m.ready(health,'production')
for key in ['generation_enabled','guardrails_embedding_loaded','guardrails_loaded']:
 assert not m.ready({**health,key:False},'testing')
assert not m.ready({**health,'guardrails_environments':['production']},'testing')
assert not m.ready({**health,'redis_session_store':'disconnected'},'testing')
assert not m.ready({},'testing')
assert not m.ready(health,'testing',True)
assert m.ready({**health,'general_knowledge_enabled':True},'testing',True)
print(json.dumps({'status':'PASS','specificEnvironmentRequired':True,'missingProductionAcceptedForTesting':True,'embeddingGenerationRedisRequired':True,'clusterCalls':0}))
