FROM aidamian/base_llm_env:latest


WORKDIR /aid_app

COPY  . /aid_app

ENV TZ Europe/Bucharest

ENV AID_APP_DOCKER Yes
ENV SHOW_PACKS Yes
ENV FORCE_CPU No
ENV AID_APP_ID NeuralEnergyAiLibrary

ENV PYTHONPATH .

EXPOSE 5001-5015/tcp

CMD ["python", "run_gateway.py"]
