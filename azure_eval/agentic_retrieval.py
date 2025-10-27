import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.agent import KnowledgeAgentRetrievalClient
from azure.search.documents.agent.models import (
    KnowledgeAgentRetrievalRequest,
    KnowledgeAgentMessage,
    KnowledgeAgentMessageTextContent,
    SearchIndexKnowledgeSourceParams,
)
from azure.ai.openai import OpenAIClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

# --- config (env vars recommended) ---
SEARCH_ENDPOINT = os.environ["AZURE_SEARCH_API_ENDPOINT"]           # e.g. "https://<your-search>.search.windows.net"
SEARCH_API_KEY = os.environ["AZURE_SEARCH_API_KEY"]                 # Admin or query key
KNOWLEDGE_AGENT_NAME = os.environ["AZURE_SEARCH_KNOWLEDGE_AGENT_NAME"]  # the agent you created in Search
AOAI_ENDPOINT = os.environ["EVALUATOR_AZURE_OPENAI_ENDPOINT"]             # e.g. "https://<your-aoai>.openai.azure.com"
AOAI_DEPLOYMENT = os.environ["EVALUATOR_AZURE_OPENAI_DEPLOYMENT"]         # e.g. "gpt-4o-mini"

# --- 1) Call agentic retrieval on Azure AI Search ---
retrieval_client = KnowledgeAgentRetrievalClient(
    endpoint=SEARCH_ENDPOINT,
    agent_name=KNOWLEDGE_AGENT_NAME,
    credential=AzureKeyCredential(SEARCH_API_KEY),
)

# Chat history + current user question (the planner uses the full thread)
messages = [
    KnowledgeAgentMessage(
        role="user",
        content=[KnowledgeAgentMessageTextContent(text="Give me a quick overview of our 2024 product roadmap.")]
    )
]

# Optional knobs for this call (filters, doc caps, etc.)
ks_params = SearchIndexKnowledgeSourceParams(
    # examples:
    # filter="category eq 'roadmap' and year eq 2024",
    # top_n_documents=200,
)

request = KnowledgeAgentRetrievalRequest(
    messages=messages,
    knowledge_source_params=ks_params,
    # Some services also accept: max_documents_for_reranker, include_references, etc.
)

retrieval_result = retrieval_client.retrieve(request)

# The key parts of the response:
grounding_chunks = retrieval_result.content.text         # unified grounding payload (string, typically JSON array of chunks)
references = retrieval_result.references                 # structured metadata per source
activity = retrieval_result.activity                     # plan + per-step telemetry

# --- 2) Ask Azure OpenAI to answer using the grounded content ---
aoai_client = OpenAIClient(endpoint=AOAI_ENDPOINT, credential=DefaultAzureCredential())

system_prompt = (
    "You are a helpful assistant. Use ONLY the provided `grounding` text to answer. "
    "Cite sources with the URI if available."
)

user_question = messages[-1].content[0].text  # same question we sent to retrieval

completion = aoai_client.chat_completions.create(
    model=AOAI_DEPLOYMENT,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Question: {user_question}\n\nGrounding:\n{grounding_chunks}"},
    ],
    temperature=0.2,
)

answer = completion.choices[0].message.content

print("\n=== Answer ===\n")
print(answer)

print("\n=== References ===\n")
for r in references or []:
    # For search-index refs you’ll typically see fields like key, indexName, etc.
    # For blob refs you’ll see container/blob info.
    print(r)
