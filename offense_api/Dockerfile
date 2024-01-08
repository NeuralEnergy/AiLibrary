FROM pytorch/pytorch

RUN pip install --no-cache-dir transformers tokenizers fastapi uvicorn

WORKDIR /offense_api

COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5050"]