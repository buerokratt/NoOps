import os
from dotenv import load_dotenv
from azure.identity import EnvironmentCredential
from azure.search.documents.indexes import SearchIndexClient
# NOTE: These two types exist only in **preview** SDKs
from azure.search.documents.indexes.models import (
    SearchIndexKnowledgeSource,
    SearchIndexKnowledgeSourceParameters,
)

load_dotenv()

endpoint = os.environ["AZURE_SEARCH_API_ENDPOINT"]
credential = EnvironmentCredential()

api_version = "2025-08-01-preview"   # required for knowledge sources
index_name = "yld-index"
knowledge_source_name = os.environ["KNOWLEDGE_SOURCE_NAME"]

ks = SearchIndexKnowledgeSource(
    name=knowledge_source_name,
    description="Knowledge source for Earth at night data",
    search_index_parameters=SearchIndexKnowledgeSourceParameters(
        search_index_name=index_name,
        source_data_select="chunk_id,chunk,title",
    ),
)

client = SearchIndexClient(endpoint=endpoint, credential=credential)
client.create_or_update_knowledge_source(
    knowledge_source=ks,
    api_version=api_version
)
print(f"Knowledge source '{knowledge_source_name}' created or updated successfully.")
