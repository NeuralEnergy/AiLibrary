docker build -t aidamian/llm_api .
docker image prune -f
docker push aidamian/llm_api