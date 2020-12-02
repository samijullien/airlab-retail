#!/bin/bash

CMD="$1"

if [[ $CMD == "create" ]]; then
    # Deploy the container group
    az container create --resource-group airlab --file $(dirname $0)/azure_container_group.yaml
elif [[ $CMD == "show" ]]; then
    # View deployment state
    az container show --resource-group airlab --name retailContainerGroup --output table
elif [[ $CMD == "logs" ]]; then
    # View container logs
    az container logs --resource-group airlab --name retailContainerGroup --container-name retail-web
elif [[ $CMD == "delete" ]]; then
    # Delete the container group
    az container delete --resource-group airlab --name retailContainerGroup
else
    echo "Unknown command '$1'"
fi