# router.py
import json
from schemas import SERVICE_SCHEMAS
from intents import intent_embeddings, model
from classifier import detect_intent, is_confident_enough
from extractors import EXTRACTORS
from utils import is_informative, normalize_input
from sentence_transformers import util

def has_valid_params(params):
    return any(v is not None and str(v).strip() != "" for v in params.values())

def extract_params(intent_name, text):
    schema = SERVICE_SCHEMAS.get(intent_name, {})
    results = {}
    for param, info in schema.get("params", {}).items():
        if param in results:
            continue
        if "extract" in info:
            extractor_fn = EXTRACTORS[info["extract"]]
            value = extractor_fn(text)
        else:
            value = None
        if isinstance(value, dict):
            results.update(value)
        elif value is not None:
            results[param] = value
        elif info.get("required", False):
            results[param] = None
    return results

# Full query routing, now taking settings as arguments
def route_query(text, enforce_params=True, threshold=0.8):
    if not is_informative(text):
        return {"route": "RAG", "intent": "general_question", "confidence": 1.0, "reason": "not_informative"}

    normalized = normalize_input(text)
    intent, confidence = detect_intent(normalized)

    # Get top 2 scores
    query_vec = model.encode(text, convert_to_tensor=True)
    top_scores = sorted([
        util.cos_sim(query_vec, embs).max().item()
        for embs in intent_embeddings.values()
    ], reverse=True)[:2]

    if not is_confident_enough(confidence, text, top_scores):
        return {
            "route": "RAG",
            "intent": "general_question",
            "confidence": confidence,
            "reason": f"low_confidence (best intent: {intent}, score={confidence})"
        }

    params = extract_params(intent, text)

    if intent not in SERVICE_SCHEMAS:
        return {"route": "SERVICE", "intent": intent, "confidence": confidence, "params": {}}

    if enforce_params:
        if not has_valid_params(params):
            return {"route": "RAG", "intent": "general_question", "confidence": confidence, "reason": "invalid_params"}

        missing = [k for k, v in params.items() if v is None]
        if missing:
            return {
                "route": "INCOMPLETE",
                "intent": intent,
                "confidence": confidence,
                "missing_params": missing,
                "recognized": params
            }

    return {"route": "SERVICE", "intent": intent, "confidence": confidence, "params": params}
