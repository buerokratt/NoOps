#!/bin/bash

NAMESPACE=""
RELEASE_NAME=""
CHARTS=()

usage() {
  echo "Usage: $0 -n <namespace> -r <release_name> -c <chart> [-c <chart> ...]" >&2
  exit 1
}

while getopts ":n:r:c:" option; do
  case $option in
    n)
      NAMESPACE=$OPTARG
      ;;
    r)
      RELEASE_NAME=$OPTARG
      ;;
    c)
      CHARTS+=("$OPTARG")
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      usage
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      usage
      ;;
  esac
done

if [ -z "$NAMESPACE" ] || [ -z "$RELEASE_NAME" ] || [ ${#CHARTS[@]} -eq 0 ]; then
  echo "Namespace, release name, and at least one chart are required."
  usage
fi

for CHART in "${CHARTS[@]}"; do
  case $CHART in
    pipeline)
      echo "Installing pipeline chart"
       helm install "$RELEASE_NAME" ../../Kubernetes/Post-deploy/pipeline -n "$NAMESPACE"
      ;;
    first-login)
      echo "Installing first-login chart"
       helm install "$RELEASE_NAME" ../../Kubernetes/Post-deploy/first-login -n "$NAMESPACE"
      ;;
    dmapperv1)
      echo "Installing dmapperv1 chart"
       helm install "$RELEASE_NAME" ../../Kubernetes/Post-deploy/dmapperv1 -n "$NAMESPACE"
      ;;
    byk-bot)
      echo "Installing byk-bot chart"
       helm install "$RELEASE_NAME" ../../Kubernetes/Components/Bot -n "$NAMESPACE"
      ;;
    *)
      echo "Invalid chart specified: $CHART" >&2
      usage
      ;;
  esac
done
