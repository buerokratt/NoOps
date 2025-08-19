# intents.py
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("sentence-transformers/LaBSE")

# Define service intents
service_intents = {
    "weather_query": [
        "mis ilm on praegu",
        "tahan teada ilma",
        "kuidas on ilm Tartus",
        "milline on ilm täna"
    ],
    "document_request": [
        "soovin id kaarti",
        "uus isikut tõendav dokument",
        "taotle uut ID-kaarti",
        "kuidas uut id kaarti taotleda"
    ],
    "vehicle_tax_check": [
        "kui suur on sõiduki aastamaks",
        "palju pean automaksu maksma",
        "mootorsõiduki maksu päring",
        "automaks reg nr",
        "kui palju pean maksma sõiduki eest",
        "kui suur on automaks"
    ],
    "electricity_info": [
        "kui kallis on elekter praegu",
        "mis kell on täna kõige odavam elekter",
        "millal on elekter kallis",
        "mis on praegune elektri hind"
    ],
    "holiday_info": [
        "milline on järgmine riigipüha",
        "kas täna on püha",
        "millal oli viimati riigipüha",
        "millal on võidupüha",
        "mis püha täna on"
    ],
    "currency_conversion": [
        "mitu dollarit on üks euro",
        "mis on euro ja jeeni vaheline kurss",
        "kui palju on sada dollarit eurodes",
        "euro ja usd vaheline kurss"
    ],
    "recent_votes": [
        "millised olid viimased riigikogu hääletused",
        "viimane hääletus parlamendis",
        "mille üle on hiljuti parlamendis hääletatud",
        "viimane parlamendi hääletus"
    ],
    "backoffice": [
        "soovin suhelda klienditeenindajaga",
        "palun nõustajat",
        "suuna mind",
        "suuna mind klienditeenindajale",
        "suuna teenindajale"
    ]
}

# Precompute embeddings
intent_embeddings = {
    intent: model.encode(samples, convert_to_tensor=True)
    for intent, samples in service_intents.items()
}