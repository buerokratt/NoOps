import os
from dotenv import load_dotenv
import time

load_dotenv()

#Map LangChain's default field names to your index schema BEFORE importing AzureSearch
os.environ["AZURESEARCH_FIELDS_ID"] = "chunk_id"
os.environ["AZURESEARCH_FIELDS_CONTENT"] = "chunk"
os.environ["AZURESEARCH_FIELDS_CONTENT_VECTOR"] = "text_vector"
# os.environ["AZURESEARCH_FIELDS_TAG"] = "title"

from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings
import pandas as pd

index_name: str = os.environ["INDEX_NAME"]
df = pd.read_excel("datasets/eestiee_dataset.xlsx")

AZURE_OPENAI_AI_ENDPOINT = os.getenv("AZURE_OPENAI_AI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME")
AZURE_SEARCH_API_ENDPOINT = os.getenv("AZURE_SEARCH_API_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")

AZURE_OPENAI_API_VERSION = "2025-01-01-preview"

embeddings = AzureOpenAIEmbeddings(
    azure_deployment=AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME,
    openai_api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_AI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
)

vector_store = AzureSearch(
    azure_search_endpoint=AZURE_SEARCH_API_ENDPOINT,
    azure_search_key=AZURE_SEARCH_API_KEY,
    index_name=index_name,
    embedding_function=embeddings.embed_query,
    additional_search_client_options={"retry_total": 4},
    # search_type="similarity",  # optional: vector only
)
# --- Stopwatch start ---
t0 = time.perf_counter()
df["context"] = df["query"].apply(
    lambda q: [doc.page_content for doc in vector_store.similarity_search(q, k=5)]
)
t1 = time.perf_counter()
elapsed = t1 - t0
num_queries = df["query"].notna().sum()
per_query = (elapsed / num_queries) if num_queries else float("nan")
print(f"Retrieval took {elapsed:.3f} seconds for {num_queries} queries "
      f"(~{per_query:.3f} s/query).")
#for _, row in df.iterrows():
#    print(row.to_dict())

#save the df to a new excel file.
df.to_excel("datasets/eestiee_dataset_with_context.xlsx",index=False)