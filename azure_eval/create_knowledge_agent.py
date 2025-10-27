# create_knowledge_agent_rest.py
import os, json, requests
from dotenv import load_dotenv
from azure.identity import EnvironmentCredential

load_dotenv()

# --- Required env vars (double-check names/values) ---
SEARCH_ENDPOINT = os.environ["AZURE_SEARCH_API_ENDPOINT"] # e.g. https://<name>.search.windows.net
KNOWLEDGE_SOURCE_NAME = os.environ["KNOWLEDGE_SOURCE_NAME"]
KNOWLEDGE_AGENT_NAME  = os.environ["KNOWLEDGE_AGENT_NAME"]
print(f"KNOWLEDGE_AGENT_NAME{KNOWLEDGE_AGENT_NAME}")
# Azure OpenAI config
AOAI_ENDPOINT  = os.environ["AZURE_OPENAI_AI_ENDPOINT"]           # e.g. https://<your-aoai>.openai.azure.com
AOAI_DEPLOYMENT_ID = os.environ["EVALUATOR_AZURE_OPENAI_DEPLOYMENT"]
AOAI_MODEL_NAME = os.environ["EVALUATOR_AZURE_OPENAI_DEPLOYMENT"]
AOAI_API_KEY = os.environ["AZURE_OPENAI_API_KEY"]       # optional if you use RBAC to AOAI

API_VERSION = "2025-08-01-preview"

# Acquire token for Azure AI Search
cred = EnvironmentCredential()
token = cred.get_token("https://search.azure.com/.default").token

payload = {
  "name": KNOWLEDGE_AGENT_NAME,
  "knowledgeSources": [
    {"name": KNOWLEDGE_SOURCE_NAME, "rerankerThreshold": 2.5}
  ],
  "models": [
    {
      "kind": "azureOpenAI",
      "azureOpenAIParameters": {
        "resourceUri": AOAI_ENDPOINT,
        "deploymentId": AOAI_DEPLOYMENT_ID,
        "modelName": AOAI_MODEL_NAME,
        # include apiKey if you are NOT using RBAC/managed identity to the AOAI resource:
        **({"apiKey": AOAI_API_KEY} if AOAI_API_KEY else {})
      }
    }
  ],
  "outputConfiguration": {"modality": "answerSynthesis"}
}

url = f"{SEARCH_ENDPOINT}/agents('{KNOWLEDGE_AGENT_NAME}')?api-version={API_VERSION}"
resp = requests.put(
    url,
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    data=json.dumps(payload)
)
print(f"resp : {resp}")
try:
    resp.raise_for_status()
except requests.HTTPError:
    print("Status:", resp.status_code)
    print("Body:", resp.text)
    raise

print("Created/updated knowledge agent")
