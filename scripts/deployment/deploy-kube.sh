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

# Get all running namespaces
running_namespaces=($(kubectl get namespaces --no-headers -o custom-columns=":metadata.name"))

# Create namespaces that does not exist
for element in "${selected_namespaces[@]}"; do
    if [[ ! " ${running_namespaces[*]} " =~ " ${element} " ]]; then
        echo `kubectl create namespace $element`
    fi
done

# Components
components_pod_names=("component-byk-dmapper" "component-notification-node" "component-opensearch-node" "component-byk-ruuter-private" 
"component-byk-resql" "component-byk-ruuter" "component-byk-tim")

# Modules
module_pod_names=("module-byk-analytics-gui" "module-byk-authentication-layer" "module-byk-backoffice-gui" "module-byk-services-gui" 
"module-byk-training-gui" "module-byk-widget")

# Extract Components & Modules from selected pods
selected_components=()
selected_modules=()

for pod in "${selected_pods[@]}"; do
  if [[ $pod == component* ]]; then
    selected_components+=("$pod")
  elif [[ $pod == module* ]]; then
    selected_modules+=("$pod")
  fi
done

# Get all running pods
running_pods=($(kubectl get pods -n byrokratt --no-headers -o custom-columns=":metadata.name"))

# Extract Components & Modules from running pods
running_components=()
running_modules=()

for pod in "${running_pods[@]}"; do
  if [[ $pod == component* ]]; then
    running_components+=("$pod")
  elif [[ $pod == module* ]]; then
    running_modules+=("$pod")
  fi
done

# Check if there are selected pods
if [[ -z $selected_pods ]]; then
    # deploy all pods
    non_running_components=()
    for element in "${components_pod_names[@]}"; do
      if [[ ! " ${running_components[*]} " =~ " ${element} " ]]; then
          non_running_components+=("$element")
      fi
    done

    non_running_modules=()
    for element in "${module_pod_names[@]}"; do
      if [[ ! " ${running_modules[*]} " =~ " ${element} " ]]; then
          non_running_modules+=("$element")
      fi
    done

    if [[ -n $non_running_components ]]; then echo `helm install ${non_running_components[@]} ./Components --namespace ${selected_namespaces[@]}`; fi
    if [[ -n $non_running_modules ]]; then echo `helm install ${non_running_modules[@]} ./Modules --namespace ${selected_namespaces[@]}`; fi

    if [[ -n $running_components ]]; then echo `helm upgrade ${running_components[@]} ./Components --namespace ${selected_namespaces[@]}`; fi
    if [[ -n $running_modules ]]; then echo `helm upgrade ${running_modules[@]} ./Modules --namespace ${selected_namespaces[@]}`; fi
else
    # Deploy selected components
    non_existing_selected_components=()
    for element in "${selected_components[@]}"; do
      if [[ ! " ${running_components[*]} " =~ " ${element} " ]]; then
          non_existing_selected_components+=("$element")
      fi
    done

    existing_selected_components=()
    for element in "${selected_components[@]}"; do
      if [[ ! " ${non_existing_selected_components[*]} " =~ " ${element} " ]]; then
          existing_selected_components+=("$element")
      fi
    done

    if [[ -n $non_existing_selected_components ]]; then echo `helm install ${non_existing_selected_components[@]} ./Components --namespace ${selected_namespaces[@]}`; fi
    if [[ -n $existing_selected_components ]]; then echo `helm upgrade ${existing_selected_components[@]} ./Components --namespace ${selected_namespaces[@]}`; fi

    # Deploy selected modules
    non_existing_selected_modules=()
    for element in "${selected_modules[@]}"; do
      if [[ ! " ${running_modules[*]} " =~ " ${element} " ]]; then
          non_existing_selected_modules+=("$element")
      fi
    done

    existing_selected_modules=()
    for element in "${selected_modules[@]}"; do
      if [[ ! " ${non_existing_selected_modules[*]} " =~ " ${element} " ]]; then
          existing_selected_modules+=("$element")
      fi
    done

    if [[ -n $non_existing_selected_modules ]]; then echo `helm install ${non_existing_selected_modules[@]} ./Modules --namespace ${selected_namespaces[@]}`; fi
    if [[ -n $existing_selected_modules ]]; then echo `helm upgrade ${existing_selected_modules[@]} ./Modules --namespace ${selected_namespaces[@]}`; fi
fi
