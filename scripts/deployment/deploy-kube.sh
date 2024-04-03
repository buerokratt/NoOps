#!/bin/bash

selected_pods=("$@")

components_pod_names=("byk-dmapper" "notification-node" "opensearch-node" "tim" "byk-ruuter-private" 
"byk-resql" "byk-ruuter" "byk-tim")

module_pod_names=("byk-analytics-gui" "byk-backoffice-login" "byk-backoffice-gui" "byk-services-gui" 
"byk-training-gui" "byk-widget")

# Get all running pods
running_pods=($(docker container ls --format '{{.Names }}' | tr -s ":") ) # TODO get all running pod names

# Get all non running pods
non_existing_pods=()
for element in "${pod_names[@]}"; do
    if [[ ! " ${running_pods[*]} " =~ " ${element} " ]]; then
        non_existing_pods+=("$element")
    fi
done

# echo "Running Pods: ${running_pods[@]}"
# echo "----------------------------------"
# echo "Non Running Pods: ${non_existing_pods[@]}"


if [[ -z $selected_pods ]]; then
    echo "Deploying all pods"

    echo `helm upgrade --install ${running_pods[@]} ./Modules --namespace byk-test`;
    # for pod in "${running_pods[@]}"; do
    #     echo "Deploying $pod"
    # done

    echo `helm upgrade analytics-module ./Modules/ --namespace byk-test`;
    # for pod in "${non_existing_pods[@]}"; do
    #     echo "Deploying $pod"
    # done
else
    echo "Deploying selected pods"
    echo "Selected pods: ${selected_pods[1]}"
    # for pod in "${selected_pods[@]}"; do
    #     echo "Deploying $pod"
    # done
fi
