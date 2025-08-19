# MiniLM Service Intent Classifier **POC**

A lightweight, intent-based classifier for service queries, supporting both interactive and batch processing. The script performs **intent classification**, **parameter extraction**, and routes queries to the appropriate service or fallback (RAG/general_response).

---

## Project Structure

```
minilm-test/
│── main.py               # CLI entrypoint (interactive + batch)
│── config.py             # Flags for parameter enforcement and threshold
│── router.py             # Routes queries, extracts and validates required parameters.
│── classifier.py         # Intent detection and similarity scoring.
│── extractors.py         # Entity extraction logic
│── schemas.py            # Service schemas
│── intents.py            # Service intents + embeddings
│── utils.py              # Utility functions (normalize_text, fuzzy_any, etc.)
└── requirements.txt      # Deps
```

---

## Features

- **Intent Classification**: Detects user intent using sentence-embeddings model (default: LaBSE).  
- **Parameter Extraction**: Extracts required parameters via regex, gazetteers, or custom extractors. **Needs work** 
- **Routing**: Routes queries to:
  - `SERVICE` → when intent (and required params) is recognized  
  - `INCOMPLETE` → when required params are missing (if params required) 
  - `RAG/general_question` → fallback for low-confidence or generic queries not defined as service intents
- **Interactive CLI**: Type queries directly and get instant feedback.  
- **Batch Processing**: Process queries from a text file and save results to JSON.

---

## Install Dependencies:

- `sentence-transformers` (LaBSE by default)
- `torch`
- `rapidfuzz`

Install deps via:

```
pip install -r requirements.txt
```

---

## Usage

### Interactive Mode:

Run the script interactively:

```
python3 main.py
```

Type a query and press Enter. Type `exit` or `quit` to leave.

### Batch Mode:

Process a file of queries automatically:

```
python3 main.py input.txt output.txt
```

- `input.txt` → each line is a test query
- `output.txt` → results written in JSON format (default: `results.txt`)

---

## Configuration Flags
- `--no-params` → disables required parameter enforcement (intent classification only)
- `--threshold <value>` → override the confidence threshold for intent classification (default: 0.8)

Example:

```
python3 main.py input.txt output.txt --no-params --threshold 0.75
```

---

## Adding New Intents

1. Add the new intents and few-shot examples in `intents.py`
2. Precompute embeddings (automatically done in `intents.py`)
3. Define the required parameters in `schemas.py`
4. Create parameter extraction logic in `extractors.py` (if required)

---
