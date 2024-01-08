docker build -t aidamian/llm_api_gpu -f Dockerfile_gpu .
docker image prune -f
docker run --name offense_api_gpu --gpus=all --rm -p 5051:5051 -v llm_api_vol:/offense_api/_models_cache aidamian/llm_api_gpu