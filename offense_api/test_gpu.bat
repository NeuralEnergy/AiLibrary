call build.bat
docker run --name offense_api_gpu --gpus=all --rm -p 5081:5081 -e PORT=5081 -v llm_api_vol:/offense_api/_models_cache aidamian/ro_offense_api