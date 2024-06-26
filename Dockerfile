FROM aidamian/base_th_llm_fastapi:latest


WORKDIR /aid_app

COPY  . /aid_app


ENV AID_APP_SHOW_PACKS Yes
ENV AID_APP_FORCE_CPU No

ENV AID_APP_DOCKER Yes
ENV AID_APP_ID NeuralEnergyAiLibrary

ENV NEAIL_VERSION 1.1.0

ENV PYTHONPATH .

EXPOSE 5001-5015/tcp

CMD ["python", "run_gateway.py"]
