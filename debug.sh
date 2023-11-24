#!/bin/bash
# first we check that the dev-container is correctly running by checking the env
# if the AID_APP_DOCKER is not set to "Yes" we exit
if [ "$AID_APP_DOCKER" != "Yes" ]; then
    echo "The dev container is not running. Please run the dev container and try again."
    exit 1
fi
python run_gateway.py