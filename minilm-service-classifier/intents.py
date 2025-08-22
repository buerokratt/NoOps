# intents.py
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("sentence-transformers/LaBSE")

# Define service intents
service_intents = {
    "document_request": [
        "soovin id kaarti",
        "uus isikut tõendav dokument",
        "taotle uut ID-kaarti",
        "kuidas uut id kaarti taotleda"
    ],
    "common_service_weather": [
        "mis ilm on praegu",
        "tahan teada ilma",
        "kuidas on ilm Tartus",
        "milline on ilm täna",
        "ilma päring",
        "kas praegu on ilus ilm"
    ],
    "common_service_motor_vehicle_tax": [
        "kui suur on sõiduki aastamaks",
        "palju pean automaksu maksma",
        "mootorsõiduki maksu päring",
        "automaks reg nr",
        "kui palju pean maksma sõiduki eest",
        "kui suur on automaks"
    ],
    "common_service_electricity_price": [
        "kui kallis on elekter praegu",
        "mis kell on täna kõige odavam elekter",
        "millal on elekter kallis",
        "mis on praegune elektri hind"
    ],
    "common_service_holidays": [
        "milline on järgmine riigipüha",
        "kas täna on püha",
        "millal oli viimati riigipüha",
        "millal on võidupüha",
        "mis püha täna on"
    ],
    "common_service_exchange_rate": [
        "mitu dollarit on üks euro",
        "mis on euro ja jeeni vaheline kurss",
        "kui palju on sada dollarit eurodes",
        "euro ja usd vaheline kurss"
    ],
    "common_service_parliament_votes": [
        "millised olid viimased riigikogu hääletused",
        "viimane hääletus parlamendis",
        "mille üle on hiljuti parlamendis hääletatud",
        "viimane parlamendi hääletus"
    ],
    "common_service_CPI": [
        "mis on eesti tarbijahinnaindeks",
        "kui suur on tarbija hinna indeks",
        "milline on inflatsioonimäär",
        "mis on hetkel kehtiv tarbija hinnaindeks",
        "mis on THI",
        "kui palju muutus thi viimase aastaga"
    ],
    "common_service_estimated_subsistence_minimum": [
        "arvestuslik elatusmiinimum",
        "kui suur on elatusmiinimum",
        "palju on leibkonna elatusmiinimum",
        "milline on arvestuslik elatusmiinimum",
        "elatusmiinimumi määr",
        "elatus miinimum ühe inimese kohta"
    ],
    "common_service_nba_results": [
        "mis olid viimaste mängude tulemused NBA-s",
        "kuidas läks viimastel nba mängudel",
        "kuidas lõppes viimane nba kohtumine",
        "mis oli eilse nba mängu tulemus",
        "nba mängude tulemused",
        "kes võitis viimase nba mängu"
    ],
    "common_service_unemployment_rate": [
        "kui palju on töötuid",
        "mis on töötuse määr eestis",
        "palju on eestis töötuid",
        "kui palju inimesi eestis ei tööta",
        "töötuse määr",
        "kui suur on eestis töötute osakaal"
    ],
    "common_teenus_citizien_initiative": [
        "mis on viis viimast avalikku algatust",
        "kas saate loetleda viis viimast avalikku algatust",
        "viimased avalikud algatused",
        "millised on viimased populaarsed rahvaalgatused",
        "rahvaalgatuste info",
        "soovin teavet rahvaalgatuste kohta"
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
