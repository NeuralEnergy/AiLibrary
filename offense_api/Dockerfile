#
# Neural Energy Power Plant project 
#
# @Author: Neuroplastic Software SRL
# @Copyright: Neural Energy SRL
# @description: Dockerfile for the CPU version of the API
# @Date: 2022-10-01
# @Last Modified by:   Neuroplastic Software SRL
# 

FROM pytorch/pytorch

RUN pip install --no-cache-dir transformers tokenizers fastapi uvicorn

WORKDIR /offense_api

COPY main.py .
COPY README.md .

# Set an environment variable for the port with a default value
ENV PORT=5050

# Use the environment variable in the CMD instruction
CMD uvicorn main:app --host 0.0.0.0 --port $PORT