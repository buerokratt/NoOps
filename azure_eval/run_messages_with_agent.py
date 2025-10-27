import os
import json
import time
import pathlib
import requests
from typing import Dict, Any, Iterable
from dotenv import load_dotenv
load_dotenv()
from azure.identity import EnvironmentCredential, DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.agent import KnowledgeAgentRetrievalClient
from azure.search.documents.agent.models import (
    KnowledgeAgentRetrievalRequest, KnowledgeAgentMessage,
    KnowledgeAgentMessageTextContent, SearchIndexKnowledgeSourceParams
)
from azure.ai.evaluation import AzureOpenAIModelConfiguration, GroundednessEvaluator, RelevanceEvaluator, evaluate


SEARCH_ENDPOINT = os.environ["AZURE_SEARCH_API_ENDPOINT"]   # https://<name>.search.windows.net
KNOWLEDGE_AGENT_NAME = os.environ["KNOWLEDGE_AGENT_NAME"]
KNOWLEDGE_SOURCE_NAME = os.environ["KNOWLEDGE_SOURCE_NAME"]
API_VERSION = "2025-08-01-preview"

key = os.getenv("AZURE_SEARCH_API_KEY")

if key:
    credential = AzureKeyCredential(key)
else:
    credential = EnvironmentCredential()

agent_client = KnowledgeAgentRetrievalClient(
    endpoint=SEARCH_ENDPOINT,
    agent_name=KNOWLEDGE_AGENT_NAME,
    credential=credential,
    api_version=API_VERSION,
    audience="https://search.azure.com",  # important for Entra ID
)
query_1 = """
Tere, Kui kaua võtaks aega elamisõiguse taotlus Eesti välisesinduses ja kui taotlus täidetakse, kas siis antakse mingi paber-või digidokument? Taotleja on EL kodanik ja Eesti kodaniku pereliige.
"""

messages = [
    KnowledgeAgentMessage(role="user", content=[KnowledgeAgentMessageTextContent(text=query_1)])
]

req = KnowledgeAgentRetrievalRequest(
    messages=messages,
    knowledge_source_params=[SearchIndexKnowledgeSourceParams(knowledge_source_name=KNOWLEDGE_SOURCE_NAME)]
)

result = agent_client.retrieve(retrieval_request=req)
print("OK", result)

response_contents = []
activity_contents = []
references_contents = []

response_parts = []
if getattr(result, "response", None):
    for resp in result.response:
        for content in getattr(resp, "content", []):
            text = getattr(content, "text", None) or getattr(content, "value", None) or str(content)
            response_parts.append(text)
response_content = "\n\n".join(response_parts) if response_parts else "No response found on 'result'"

response_contents.append(response_content)

# Print the three string values
print("response_content:\n", response_content, "\n")

messages.append({
    "role": "assistant",
    "content": response_content
})

# Activity -> JSON string of activity as list of dicts
if getattr(result, "activity", None):
    activity_content = json.dumps([a.as_dict() for a in result.activity], indent=2)
else:
    activity_content = "No activity found on 'result'"
    
activity_contents.append(activity_content)
print("activity_content:\n", activity_content, "\n")

# References -> JSON string of references as list of dicts
if getattr(result, "references", None):
    references_content = json.dumps([r.as_dict() for r in result.references], indent=2)
else:
    references_content = "No references found on 'result'"
    
references_contents.append(references_content)
print("references_content:\n", references_content)

foundry_endpoint = "https://bykrag.services.ai.azure.com/api/projects/bykProject"
aoai_api_version = os.environ["AOAI_API_VERSION"]

evaluation_data = []
print("Preparing evaluation data...")
for q, r, g in zip(query_1, references_contents, response_contents):
    evaluation_data.append({
        "query": q,
        "response": g,
        "context": r,
    })

filename = "evaluation_data.jsonl"

with open(filename, "w") as f:
    for item in evaluation_data:
        f.write(json.dumps(item) + "\n")

aoai_endpoint = os.environ["EVALUATOR_AZURE_OPENAI_ENDPOINT"]
aoai_gpt_model = os.environ["EVALUATOR_AZURE_OPENAI_DEPLOYMENT"]

model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=aoai_endpoint,
    api_version=aoai_api_version,
    azure_deployment=aoai_gpt_model
)

# RAG triad metrics
groundedness = GroundednessEvaluator(model_config=model_config)
relevance = RelevanceEvaluator(model_config=model_config)

print("Starting evaluation...")
result = evaluate(
    data=filename,
    evaluators={
        "groundedness": groundedness,
        "relevance": relevance,
    },
    azure_ai_project=foundry_endpoint,
)

print("Evaluation complete.")
studio_url = result.get("studio_url")
print("For more information, go to the Azure AI Foundry portal.") if studio_url else None

