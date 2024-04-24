#!/bin/bash

selected_namespaces=()
selected_pods=()

# Read Inputs
while [[ $# -gt 0 ]]; do
    case $1 in
        -n)
            shift
            while [[ $# -gt 0 && ! $1 == -* ]]; do
                selected_namespaces+=("$1")
                shift
            done
            ;;
        -p)
            shift
            while [[ $# -gt 0 && ! $1 == -* ]]; do
                selected_pods+=("$1")
                shift
            done
            ;;
        *)
            echo "Invalid option: $1" >&2
            exit 1
            ;;
    esac
done

# Check if namespaces are provided
if [[ -z $selected_namespaces ]]; then
    echo "Namespaces are required, Use -n flag to specify namespaces"
    exit 1
fi

# Remove any duplicates
selected_namespaces=($(echo "${selected_namespaces[@]}" | tr ' ' '\n' | sort -u | tr '\n' ' '))
selected_pods=($(echo "${selected_pods[@]}" | tr ' ' '\n' | sort -u | tr '\n' ' '))

# Get all running pods
running_pods=($(helm ls --short --namespace ${selected_namespaces[@]}))
jobs=($(kubectl get jobs --namespace ${selected_namespaces[@]} --no-headers -o custom-columns=":metadata.name"))

# Check if there are running pods
if [[ -z $running_pods ]]; then
    echo "No running pods found."
    exit 1
fi

# Check if there are no selected pods
if [[ -z $selected_pods ]]; then
    # Uninstall all running pods
    for element in "${running_pods[@]}"; do
        echo `helm uninstall ${element} --namespace ${selected_namespaces[@]}`;
    done
else
    # Uninstall selected pods
    existing_selected_pods=()
    for element in "${selected_pods[@]}"; do
     if [[ "${running_pods[*]}"  =~ (^|[[:space:]])"$element"($|[[:space:]]) ]]; then
       existing_selected_pods+=("$element")
     fi
    done

    if [[ -z $existing_selected_pods ]]; then
        echo "None of the selected pods are running on the given namespaces."
        exit 1
    fi

    for element in "${existing_selected_pods[@]}"; do
        echo `helm uninstall ${element} --namespace ${selected_namespaces[@]}`;
    done
fi

# Delete jobs
echo `kubectl delete jobs ${jobs}` 
