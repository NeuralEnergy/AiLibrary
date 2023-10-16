docker rmi local_ne
docker build -t local_ne .
docker run --rm --name local_ne -p 5002-5010:5002-5010 --env-file ./.env local_ne