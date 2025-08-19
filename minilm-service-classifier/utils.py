# utils.py
import re, unicodedata
from rapidfuzz import fuzz

FILLER_INPUTS = {"jep", "jah", "ok", "okei", "hmm", "lol", "wtf", "??", "...", "ei", "eip"}

# Normalize diacritics (ä → a, õ → o, etc.)
def normalize_text(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()

# Fuzzy match one keyword against words in the text
def fuzzy_contains(text, keyword, threshold=85):
    words = re.findall(r'\w+', normalize_text(text))
    norm_kw = normalize_text(keyword)
    return any(fuzz.ratio(word, norm_kw) >= threshold for word in words)

# Fuzzy check if any of the keywords exist
def fuzzy_any(text, keywords, threshold=85):
    return any(fuzzy_contains(text, kw, threshold) for kw in keywords)

# Normalize inputs (remove punctuation)
def normalize_input(text):
    return text.strip().rstrip(".!?")

# Filter junk intents
def is_informative(text):
    return len(text.strip()) >= 3 and text.lower() not in FILLER_INPUTS