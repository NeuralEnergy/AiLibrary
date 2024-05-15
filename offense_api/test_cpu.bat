call build.bat
docker run --name offense_api_cpu --rm -p 5080:5080 -e PORT=5080 -v llm_api_vol:/offense_api/_models_cache aidamian/ro_offense_api