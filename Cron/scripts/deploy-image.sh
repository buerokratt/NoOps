#!/bin/bash

##Need to check client list and backup locations. Value of "client_list" will be clients, that will be updated.
client_list=byrokratt
for client in $client_list; do
    if [ ! -d ./BACKUPS/$client ]; then
        echo "$client is not set"
        exit 1
    fi
done
echo "client list looks good"


##MasterSecrets.yaml to get all new versions
. "MasterSecrets.env"
##Replacing placeholders in all clients secrets.yaml with new values
for client in $client_list; do
    sed -i "s/component_bot_image_version/$component_bot_image_version/g" "$client/secrets.yaml"
    sed -i "s/component_ruuter_image_version/$component_ruuter_image_version/g" "$client/secrets.yaml"
    sed -i "s/component_resql_image_version/$component_resql_image_version/g" "$client/secrets.yaml"
    sed -i "s/component_tim_image_version/$component_tim_image_version/g" "$client/secrets.yaml"
    sed -i "s/component_cronmanager_image_version/$component_cronmanager_image_version/g" "$client/secrets.yaml"
    sed -i "s/component_datamapper_image_version/$component_datamapper_image_version/g" "$client/secrets.yaml"
    sed -i "s/component_notification_node_image_version/$component_notification_node_image_version/g" "$client/secrets.yaml"
    sed -i "s|component_opensearch_node_image_version|$component_opensearch_node_image_version|g" "$client/secrets.yaml"
    sed -i "s/component_s3_ferry_image_version/$component_s3_ferry_image_version/g" "$client/secrets.yaml"
    sed -i "s/component_xtr_image_version/$component_xtr_image_version/g" "$client/secrets.yaml"
    sed -i "s/component_widget_gui_version/$component_widget_gui_version/g" "$client/secrets.yaml"
    sed -i "s/module_backoffice_image_version/$module_backoffice_image_version/g" "$client/secrets.yaml"
    sed -i "s/module_analytics_image_version/$module_analytics_image_version/g" "$client/secrets.yaml"
    sed -i "s/module_services_image_version/$module_services_image_version/g" "$client/secrets.yaml"
    sed -i "s/module_training_image_version/$module_training_image_version/g" "$client/secrets.yaml"
    sed -i "s/module_backoffice_gui_version/$module_backoffice_gui_version/g" "$client/secrets.yaml"
    sed -i "s/module_analytics_gui_version/$module_analytics_gui_version/g" "$client/secrets.yaml"
    sed -i "s/module_training_gui_version/$module_training_gui_version/g" "$client/secrets.yaml"
    sed -i "s/module_training_pipelines_version/$module_training_pipelines_version/g" "$client/secrets.yaml"
    sed -i "s/module_service_gui_version/$module_service_gui_version/g" "$client/secrets.yaml"
    sed -i "s/module_authlayer_gui_version/$module_authlayer_gui_version/g" "$client/secrets.yaml"

    ##Making copy of changed files to BACKUP/client, so that all deploys are revertable
    echo "adding copy of deploy to $client BACKUP"
    cp ./$client/secrets.yaml ./BACKUPS/$client/secrets.yaml$(date +%Y%m%d%H%M) || echo "secrets.yaml in $client folder not found"

    cd ./$client
    bash deploy.sh
    cd ../
    cp -r ./$client/NoOps ./BACKUPS/$client/NoOps$(date +%Y%m%d%H%M) || echo "NoOps in $client folder not found"
    sleep 7
done


##UPDATING all client components EXCEPT DATABASES and OPENSEARCH
for client in $client_list; do
    current_path=$(pwd)
    cd $client/NoOps/helm_deploy_v2/NoOps/Kubernetes/Components
    helm upgrade -n $client component-byk-ruuter ./Ruuter
    helm upgrade -n $client component-byk-ruuter-private ./Private-Ruuter
    helm upgrade -n $client component-byk-tim ./TIM
    helm upgrade -n $client component-byk-resql ./Resql
    helm upgrade -n $client component-byk-dmapper ./DataMapper
    helm upgrade -n $client component-byk-trainbot ./Train-bot
    helm upgrade -n $client component-byk-bot ./Bot
    helm upgrade -n $client component-byk-cronmanager ./CronManager
    helm upgrade -n $client component-byk-s3ferry ./s3Ferry
    helm upgrade -n $client component-byk-s3ferry-publish ./s3ferry-publish
    helm upgrade -n $client component-byk-notificationns-node ./Notification-server
    helm upgrade -n $client component-byk-xtr ./XTR
    cd $current_path
done

##UPDATING all client modules
for client in $client_list; do
    current_path=$(pwd)
    cd $client/NoOps/helm_deploy_v2/NoOps/Kubernetes/Modules
    helm upgrade -n $client module-byk-widget ./Widget
    helm upgrade -n $client module-byk-authentication-layer ./Authentication-Layer
    helm upgrade -n $client module-byk-backoffice-gui ./Buerokratt-Chatbot
    helm upgrade -n $client module-byk-analytics-gui ./Analytics-Module
    helm upgrade -n $client module-byk-training-module-gui ./Training-Module
    helm upgrade -n $client module-byk-service-gui ./Service-Module
    cd $current_path
    rm -rf $client/NoOps
done


##Restoring client/secrets.yaml files. Adding placeholders back again, so that script would be executable again next time
for client in $client_list; do
    sed -i "0,/$component_bot_image_version/s//component_bot_image_version/" "$client/secrets.yaml"
    sed -i "0,/$component_ruuter_image_version/s//component_ruuter_image_version/" "$client/secrets.yaml"
    sed -i "0,/$component_resql_image_version/s//component_resql_image_version/" "$client/secrets.yaml"
    sed -i "0,/$component_tim_image_version/s//component_tim_image_version/" "$client/secrets.yaml"
    sed -i "0,/$component_cronmanager_image_version/s//component_cronmanager_image_version/" "$client/secrets.yaml"
    sed -i "0,/$component_datamapper_image_version/s//component_datamapper_image_version/" "$client/secrets.yaml"
    sed -i "0,/$component_notification_node_image_version/s//component_notification_node_image_version/" "$client/secrets.yaml"
    # "0,/$component_opensearch_node_image_version/s|$component_opensearch_node_image_version|component_opensearch_node_image_version|" "$client/secrets.yaml"
    sed -i "0,/$(printf '%s\n' "$component_opensearch_node_image_version" | sed 's/[\/&]/\\&/g')/s|$component_opensearch_node_image_version|component_opensearch_node_image_version|" "$client/secrets.yaml"
    sed -i "0,/$component_s3_ferry_image_version/s//component_s3_ferry_image_version/" "$client/secrets.yaml"
    sed -i "0,/$component_xtr_image_version/s//component_xtr_image_version/" "$client/secrets.yaml"
    sed -i "0,/$component_widget_gui_version/s//component_widget_gui_version/" "$client/secrets.yaml"
    sed -i "0,/$module_backoffice_image_version/s//module_backoffice_image_version/" "$client/secrets.yaml"
    sed -i "0,/$module_analytics_image_version/s//module_analytics_image_version/" "$client/secrets.yaml"
    sed -i "0,/$module_services_image_version/s//module_services_image_version/" "$client/secrets.yaml"
    sed -i "0,/$module_training_image_version/s//module_training_image_version/" "$client/secrets.yaml"
    sed -i "0,/$module_backoffice_gui_version/s//module_backoffice_gui_version/" "$client/secrets.yaml"
    sed -i "0,/$module_analytics_gui_version/s//module_analytics_gui_version/" "$client/secrets.yaml"
    sed -i "0,/$module_training_gui_version/s//module_training_gui_version/" "$client/secrets.yaml"
    sed -i "0,/$module_training_pipelines_version/s//module_training_pipelines_version/" "$client/secrets.yaml"
    sed -i "0,/$module_service_gui_version/s//module_service_gui_version/" "$client/secrets.yaml"
    sed -i "0,/$module_authlayer_gui_version/s//module_authlayer_gui_version/" "$client/secrets.yaml"
done


echo "done"
