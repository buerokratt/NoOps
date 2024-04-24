#!/bin/bash


NAMESPACE=""
RELEASE_NAME=""


usage() {
  echo "Usage: $0 -n <namespace> -p <release_name>" >&2
  exit 1
}


while getopts ":n:p:" option; do
  case $option in
    n)
      NAMESPACE=$OPTARG
      ;;
    r)
      RELEASE_NAME=$OPTARG
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


if [ -z "$NAMESPACE" ] || [ -z "$RELEASE_NAME" ]; then
  echo "Namespace and release name are required."
  usage
fi


helm install "$RELEASE_NAME" ../../Kubernetes/Post-deploy/pipelines -n "$NAMESPACE"
helm install "$RELEASE_NAME" ../../Kubernetes/Post-deploy/first-login -n "$NAMESPACE"
helm install "$RELEASE_NAME" ../../Kubernetes/Post-deploy/dmapperv1 -n "$NAMESPACE"