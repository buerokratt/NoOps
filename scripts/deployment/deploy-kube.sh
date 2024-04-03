#!/bin/bash

# Steps

# 1. Handle Script Inputs
# 2. Handle Namespaces
# 3. Handle Pods
# 4. Deploy OR Upgrade Pods

selected_pods=("$@")
namespaces=() # kubectl get namespaces

# Components
components_pod_names=("component-byk-dmapper" "component-notification-node" "component-opensearch-node" "component-byk-ruuter-private" 
"component-byk-resql" "component-byk-ruuter" "component-byk-tim")

# Modules
module_pod_names=("module-byk-analytics-gui" "module-byk-backoffice-login" "module-byk-backoffice-gui" "module-byk-services-gui" 
"module-byk-training-gui" "module-byk-widget")

# Get all running pods
running_pods=($(docker container ls --format '{{.Names }}' | tr -s ":") ) # in k8 = kubectl get pods -n byrokratt --no-headers -o custom-columns=":metadata.name"

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

    echo `helm upgrade module-byk-analytics-gui ./Modules/ --namespace byk-test`;
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
