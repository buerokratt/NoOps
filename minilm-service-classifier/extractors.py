# extractors.py
import re
from rapidfuzz import fuzz
from utils import normalize_text, fuzzy_any, fuzzy_contains

# Entity extractors (regex/gazetteer-based)
KNOWN_LOCATIONS = [
    "Tallinn", "Tartu", "Pärnu", "Narva", "Viljandi", "Rakvere", "Kuressaare", "Valga", "Võru", "Jõhvi", "Haapsalu", "Paide", "Keila", "Rapla", "Maardu"
]

def location_gazetteer(text):
    norm = normalize_text(text)

    for loc in KNOWN_LOCATIONS:
        norm_loc = normalize_text(loc)
        if re.search(rf"\b{norm_loc}(as|s|l|t|ni)?\b", norm):
            return loc
        # Fuzzy fallback
        if fuzz.partial_ratio(norm_loc, norm) > 85:
            return loc
    return None

def regex_plate(text):
    match = re.search(r"\b\d{3}\s?[A-Z]{3}\b", text, re.IGNORECASE)
    if match:
        return match.group(0).replace(" ", "").upper()
    return None

def regex_id_code(text):
    match = re.search(r"\b\d{11}\b", text)
    return match.group(0) if match else None

def regex_name(text):
    match = re.search(r"\b[A-ZÄÖÜÕ][a-zäöüõ]+ [A-ZÄÖÜÕ][a-zäöüõ]+\b", text)
    return match.group(0) if match else None

def regex_year(text):
    match = re.search(r"^(19|20)\d{2}$", text)
    return match.group(0) if match else None

def extract_electricity_query_type(text):
    norm = normalize_text(text)

    if fuzzy_any(norm, ["täna", "praegu", "hetke"]) or re.search(r"milline.*hind", norm):
        return "current"
    elif fuzzy_any(norm, [
        "odavaim", "odavam", "odav", "kallim", "kallis", "kõrgeim", "soodsam", "kalleim"
    ]) or re.search(r"millal.*(odavaim|kalleim)", norm):
        return "peak"
    return None

def extract_price_direction(text):
    norm = normalize_text(text)

    if fuzzy_any(norm, ["odavaim", "odav", "odavam", "soodsam", "madalaim"]):
        return "lowest"
    elif fuzzy_any(norm, ["kõrgeim", "kallim", "kallis", "kalleim"]):
        return "highest"
    return None

def extract_holiday_query_type(text):
    norm = normalize_text(text)

    if fuzzy_any(norm, ["täna", "tana"]) and fuzzy_any(norm, ["püha", "pyha", "riigipüha"]):
        return "today"
    elif fuzzy_any(norm, ["järgmine", "jargmine"]) or re.search(r"millal.*(pyha|püha|riigipüha)", norm):
        return "next"
    elif fuzzy_any(norm, ["eelmine", "viimane"]):
        return "previous"
    elif fuzzy_any(norm, ["jõulud", "uusaasta", "taasiseseisvumispäev", "võidupüha", "vabariigi aastapäev"]):
        return "specific"

    return None

def extract_holiday_name(text):
    holidays = [
        "jõulud", "uusaasta", "taasiseseisvumispäev", "võidupüha", "vabariigi aastapäev"
    ]
    norm = normalize_text(text)

    for name in holidays:
        if fuzzy_contains(norm, name):
            return name
    return None

def extract_currency_pair(text):
    currency_map = {
        r"\beuro(de|t|ga|le|l|s)?\b": "EUR",
        r"\bdollar(i|it|iga|ile|il|is|eid)?\b": "USD",
        r"\busd\b": "USD",
        r"\bgbp\b": "GBP",
        r"\bnael(a|e|i|u|t|ga|le|l|s)?\b": "GBP",
        r"\bpound(s)?\b": "GBP",
        r"\byen(i|it|iga|ile|il|is)?\b": "JPY",
        r"\bjeen(i|it|iga|ile|il|is)?\b": "JPY",
        r"\brootsi kroon(i|i|iga|ile|il|is)?\b": "SEK",
        r"\bnorra kroon(i|i|iga|ile|il|is)?\b": "NOK"
    }

    found = []
    for pattern, code in currency_map.items():
        if re.search(pattern, text, re.IGNORECASE):
            if code not in found:
                found.append(code)

    result = {}
    if len(found) == 2:
        result["source_currency"] = found[0]
        result["target_currency"] = found[1]
    elif len(found) == 1:
        result["source_currency"] = found[0]
    return result if result else None


def extract_amount(text):
    match = re.search(r"\b\d+([.,]\d+)?\b", text)
    return float(match.group(0).replace(",", ".")) if match else None

def extract_plural_votes(text):
    norm = normalize_text(text)

    if fuzzy_any(norm, ["hääletused", "hääletusi", "mitu", "viimased"]):
        return True
    elif fuzzy_any(norm, ["hääletus", "viimane", "hiljutine"]):
        return False
    return None

EXTRACTORS = {
    "location_gazetteer": location_gazetteer,
    "regex_plate": regex_plate,
    "regex_id_code": regex_id_code,
    "regex_name": regex_name,
    "extract_electricity_query_type": extract_electricity_query_type,
    "extract_price_direction": extract_price_direction,
    "extract_holiday_query_type": extract_holiday_query_type,
    "extract_holiday_name": extract_holiday_name,
    "extract_currency_pair": extract_currency_pair,
    "extract_amount": extract_amount,
    "extract_plural_votes": extract_plural_votes
}
