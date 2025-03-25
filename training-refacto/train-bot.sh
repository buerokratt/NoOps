#!/bin/bash

# Variables
# NAMESPACE=$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace) 
NAMESPACE="a1" #This value should come from Ruuter. Dont know how to achieve it as frontend to my knowldge, does not chcek or care of namespace.
HELM_REPO_NAME="train"
TRAINING_RESQL="http://resql-url"
RUUTER_BASE_URL="http://ruuter-app/api/rasa"

# Functions
get_new_nonce() {
  response=$(curl -s -X POST -H "Content-Type: application/json" "$TRAINING_RESQL/get-new-nonce")
  nonce=$(echo "$response" | grep -Eo "([a-f0-9-]+-){4}[a-f0-9-]+")
  if [[ -z "$nonce" ]]; then
    echo "Failed to retrieve nonce!" >&2
    exit 1
  fi
  echo "$nonce"
}

notify_ruuter() {
    local status="$1"
    echo "Notifying ruuter - train-bot status: ${status}"
    curl -X POST "$RUUTER_BASE_URL/train-status" \
         -H "x-ruuter-nonce: $(get_new_nonce)" \
         -H "Content-Type: application/json" \
         -d "{\"job\": \"train-bot\", \"status\": \"${status}\"}"
}

# Pre-flight Checks
if [ -z "$NAMESPACE" ]; then
    echo "Error: Failed to retrieve the namespace!" >&2
    exit 1
elif ! kubectl cluster-info &>/dev/null; then
    echo "Error: No Kubernetes cluster is available!" >&2
    exit 1
elif helm list -n "$NAMESPACE" | grep -q "train-bot"; then
    echo "Error: The Helm release 'train-bot' already exists in namespace '$NAMESPACE'. Exiting..."
    exit 1
fi

# Deploy the train-bot job
echo "Deploying train-bot job..."
helm upgrade --install train-bot "$HELM_REPO_NAME/train-bot" --namespace "$NAMESPACE" --set serviceAccount.name=train-bot-sa --create-namespace

# Wait for job to complete
echo "Waiting for train-bot job to complete..."
for ((counter=1; counter<=10; counter++)); do
    status=$(kubectl get job train-bot -n "$NAMESPACE" -o jsonpath='{.status.succeeded}')
    
    if [ "$status" == "1" ]; then
        echo "Train-bot job completed."
        notify_ruuter "completed"
        echo "Train-bot process finished!"
        exit 0
    elif [ "$counter" -eq 10 ]; then
        echo "Train-bot job failed."
        notify_ruuter "failed"
        helm uninstall train-bot --namespace "$NAMESPACE"
        exit 1
    fi
    sleep 5
done