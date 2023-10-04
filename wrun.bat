docker run --rm --name NeuralEnergy --pull=always -p 5002-5010:5002-5010 --env-file ./.env -v ai_vol:/aid_app/_cache neuralenergy/ai_library
