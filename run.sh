#!/bin/bash

while true; do
  sudo docker run --rm --name ne_ailib --pull=always -p 5002-5010:5002-5010 --env-file ./.env -v ai_vol:/aid_app/_cache neuralenergy/ai_library
  sleep 5
done
