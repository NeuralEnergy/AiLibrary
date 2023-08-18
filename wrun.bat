docker run --rm --name local_ne --pull=always -p 5002-5010:5002-5010 --env-file ./.env -v ai_vol:/aid_app/_cache safeweb/ai
