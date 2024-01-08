docker build -t aidamian/llm_api -f Dockerfile_cpu .
docker image prune -f
docker run --name offense_api_cpu --rm -p 5050:5050 -v llm_api_vol:/offense_api/_models_cache aidamian/llm_api