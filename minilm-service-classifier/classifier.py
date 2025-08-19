# classifier.py
from sentence_transformers import util
from intents import model, intent_embeddings
from utils import normalize_input

THRESHOLD = 0.8

# Intent detection
def detect_intent(user_input):
    query_vec = model.encode(user_input, convert_to_tensor=True)
    scores = {
        intent: util.cos_sim(query_vec, embs).max().item()
        for intent, embs in intent_embeddings.items()
    }
    best_intent = max(scores, key=scores.get)
    best_score = scores[best_intent]
    if best_score > THRESHOLD:
        return best_intent, round(best_score, 4)
    else:
        return "general_question", round(best_score, 4)

# Check whether top 2 intents are too similar
def is_confident_enough(confidence, input_text, top_scores):
    if len(input_text.strip()) < 5:
        return confidence > 0.88
    elif top_scores[0] - top_scores[1] < 0.05:
        return confidence > 0.85
    return confidence > 0.80
