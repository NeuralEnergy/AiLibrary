docker build -t aidamian/llm_api -f Dockerfile_cpu .
docker image prune -f
docker push aidamian/llm_api