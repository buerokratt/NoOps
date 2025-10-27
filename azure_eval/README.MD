# Azure Evaluation

## environmental variables

Here is a list of environmental variables that can be configured:
- `AI_FOUNDRY_ENDPOINT` — AI Foundry endpoint, needed to send the evaluation there.
- `AZURE_OPENAI_AI_ENDPOINT` — Needed to get to the models.
- `AZURE_OPENAI_API_KEY` — OpenAI API key that is found in AI Foundry, needed to access models.
- `AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME` — Embedding deployment name — usually has the same name as the model itself.
- `AZURE_SEARCH_API_ENDPOINT` — Endpoint for the Azure AI Search Service.
- `AZURE_SEARCH_API_KEY` — API key to use our Azure AI Search Service.
- `AOAI_API_VERSION` — AI API version that is being used.
- `AZURE_TENANT_ID` — ID of the tenant — needed to use the Azure environmental credentials.
- `AZURE_CLIENT_ID` — ID of the client — can be found under the App Registration in Entra ID for the app that has been created. Needed to use the Azure environmental credentials.
- `AZURE_CLIENT_SECRET` — Secret of the client app — provided when you created the app registration. Needed to use the Azure environmental credentials.
- `EVALUATOR_AZURE_OPENAI_ENDPOINT` — LLM-as-a-judge endpoint (e.g., `https://<PROJECT_NAME>.cognitiveservices.azure.com/`).
- `EVALUATOR_AZURE_OPENAI_DEPLOYMENT` — Model deployment used as the LLM-as-a-judge.
- `EVALUATION_PREFIX` — A short run identifier used to name outputs (JSONL and per-model result files).
š
## models/models.json configuration

Example:
```json 
[
    {
        "type": "azure-openai",
        "azure_deployment": "gpt-5",
        "azure_endpoint": "https://<PROJECT_NAME>.cognitiveservices.azure.com/"
    },
    {
        "type": "azure-openai",
        "azure_deployment": "gpt-4.1",
        "azure_endpoint": "https://<PROJECT_NAME>.cognitiveservices.azure.com/"
    }
]
```

In this file the endpoint and the deployment of the models in Azure has been defined. It is needed when we run the evaluation code.

## azure_retrieval.py

`azure_retrieval.py` enriches an input Excel dataset of queries by retrieving the top-k similar passages from an Azure AI Search vector index and appending them as a `context` column. It also logs retrieval latency per query.

### inputs / outputs

- **Input file:** `datasets/<filename>.xlsx`  
  - **Required columns:** `Id`, `query`, `ground_truth`

- **Output file:** `datasets/<filename>.xlsx`  
  - **Schema:** same as input **+** `context` (list of top-k passages per row)

### Usage

1) Populate the .env file with the necessary values
2) Run the script:
```sh
python azure_retrieval.py
```

### Configuration notes
- **Top-k:** adjust `k=5`in `similarity_search(q, k=5)` to retrieve more/fewer passages.
- **Search mode:** by default this uses vector similarity; you can set `search_type="similarity"` (already shown as a commented hint) or other supported modes if needed.
- **Retries:** `additional_search_client_options={"retry_total": 4}` provides basic resilience on transient failures.

## azure_evaluator.py

This script runs **LLM-as-a-judge** evaluations on your model endpoints using `azure.ai.evaluation`. It converts the enriched dataset to JSONL, invokes your target model(s) via a small wrapper, and scores responses for coherence, relevance, groundedness, fluency, and similarity.

### inputs / outputs
- **Input dataset** `datasets/<filename>with_context.xlsx`  
  - **Required columns:** `Id`, `query`, `ground_truth`, `context`

- **Output file:** `datasets/<filename>.xlsx`  
  - **Schema:** same as input **+** `context` (list of top-k passages per row)