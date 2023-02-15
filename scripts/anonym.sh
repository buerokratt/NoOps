#!/bin/bash
compose_path="Data-Anonymizer/Docker_Project/"
compose_to_models="anonymisation_internal/anonymisation_api/anonymise/models/"
if [ -d "$compose_path" ]; then
    echo "$compose_path already exists: checking updates from git"
    cd "$compose_path"
    git fetch
    git pull
else
    git clone https://github.com/buerokratt/Data-Anonymizer.git
    cd "$compose_path"
    docker-compose up -d
fi

if [ -d "$compose_to_models/bert_old" ] && [ -d "$compose_to_models/gdpr_model" ] && [ -d "$compose_to_models/bert_new" ] && [ -d "$compose_to_models/bert-truecaser" ]; then
    echo "correct models already exist"
else
    echo "cloning models from huggingface"
    cd "$compose_to_models"
    git clone https://huggingface.co/buerokratt/bert-truecaser && \
    git clone https://huggingface.co/buerokratt/ner_old && \
    git clone https://huggingface.co/buerokratt/ner_gdpr && \
    git clone https://huggingface.co/buerokratt/ner_new && \
    mv ner_new/ bert_new && \
    mv ner_old/ bert_old && \
    mv ner_gdpr/ gdpr_model
fi

docker-compose down
docker-compose up -d
