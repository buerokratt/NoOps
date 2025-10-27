import json
import os
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()
eval_prefix = os.getenv("EVALUATION_PREFIX")

foundry_endpoint = os.getenv("AI_FOUNDRY_ENDPOINT")

df = pd.read_excel("datasets/eestiee_dataset_with_context.xlsx")
#save to JSONL because the evaluator likes it.
data_path = f"data_json/{eval_prefix}_data.jsonl"
df.to_json(data_path, orient="records", lines=True, force_ascii=False)

evaluator_model_config = {
    "azure_endpoint" : os.getenv("EVALUATOR_AZURE_OPENAI_ENDPOINT"),
    "azure_deployment" : os.getenv("EVALUATOR_AZURE_OPENAI_DEPLOYMENT")
}

import pathlib

from azure.ai.evaluation import evaluate
from azure.ai.evaluation import (
    RelevanceEvaluator,
    CoherenceEvaluator,
    GroundednessEvaluator,
    FluencyEvaluator,
    SimilarityEvaluator
)
from model_endpoint import ModelEndpoint
relevance_evaluator = RelevanceEvaluator(evaluator_model_config)
coherence_evaluator = CoherenceEvaluator(evaluator_model_config)
groundedness_evaluator = GroundednessEvaluator(evaluator_model_config)
fluency_evaluator = FluencyEvaluator(evaluator_model_config)
similarity_evaluator = SimilarityEvaluator(evaluator_model_config)

model_json = "models/models.json"


with open(model_json) as f:
    models = json.load(f)

all_results = []
for model in models:
    eval_name = f"{eval_prefix}_{model['azure_deployment']}_without_prompt"
    print(f"Evaluating model: {model['azure_deployment']}")
    target_endpoint = ModelEndpoint(model)
    results = evaluate(
        evaluation_name=eval_name,
        data=data_path,                          # << use the path you wrote
        target=target_endpoint,                  # << your callable/endpoint wrapper
        azure_ai_project=foundry_endpoint,
        evaluators={
            # "content_safety": content_safety_evaluator,  # enable if you want safety scoring too
            "coherence": coherence_evaluator,
            "relevance": relevance_evaluator,
            "groundedness": groundedness_evaluator,
            "fluency": fluency_evaluator,
            "similarity": similarity_evaluator,
        },
        evaluator_config={
            "coherence": {
                "column_mapping": {
                    "response": "${target.response}",
                    "query": "${data.query}",
                }
            },
            "relevance": {
                "column_mapping": {
                    "response": "${target.response}",
                    "context": "${data.context}", 
                    "query": "${data.query}"
                }
            },
            "groundedness": {
                "column_mapping": {
                    "response": "${target.response}",
                    "context": "${data.context}",   
                    "query": "${data.query}"
                }
            },
            "fluency": {
                "column_mapping": {
                    "response": "${target.response}",
                    "context": "${data.context}",   
                    "query": "${data.query}"
                }
            },
            "similarity": {
                "column_mapping": {
                    "response": "${target.response}",
                    "query": "${data.query}",
                    "ground_truth": "${data.ground_truth}"
                }
            },
        },
    )

    all_results.append({"model": model["azure_deployment"], "results": results})
    with open("outputs/output_" + eval_prefix + "_" + model['azure_deployment'] + ".json", "w", encoding="utf-8") as f:
        json.dump(all_results[-1]["results"], f, indent=2, ensure_ascii=False)

