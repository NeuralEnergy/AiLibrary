# Test 1

## Input

```bash
curl --location 'localhost:5050/predict/' \
--header 'Content-Type: application/json' \
--data '{
  "text": "Tu esti cam f.r.a.i.e.r"
}'
```

## Result

```json
{
    "prediction": "Abuz (limbaj ofensiv direct, nivel ridicat de ofensivitate)",
    "metadata": {
        "version": "0.1.1",
        "worker": "fe75ddba",
        "model": "readerbench/ro-offense",
        "device": "cuda",
        "packages": [
            "fastapi                   0.108.0",
            "tokenizers                0.15.0",
            "torch                     2.1.2",
            "transformers              4.36.2"
        ],
        "elapsed_time": 0.1113,
        "average_time": 0.0905
    }
}
```

# Test 2

## Input

```bash
curl --location 'localhost:5050/predict/' \
--header 'Content-Type: application/json' \
--data '{
  "text": "Tu esti cam fraierica"
}'
```

## Result

```json
{
    "prediction": "Insulte (limbaj ofensiv direct, nivel scazut de ofensivitate)",
    "metadata": {
        "version": "0.1.1",
        "worker": "fe75ddba",
        "model": "readerbench/ro-offense",
        "device": "cuda",
        "packages": [
            "fastapi                   0.108.0",
            "tokenizers                0.15.0",
            "torch                     2.1.2",
            "transformers              4.36.2"
        ],
        "elapsed_time": 0.0673,
        "average_time": 0.0828
    }
}
```

# Test 3

## Input

```bash
curl --location 'localhost:5050/predict/' \
--header 'Content-Type: application/json' \
--data '{
  "text": "Esti destept!"
}'
```

## Result

```json
{
    "prediction": "Limbaj non-ofensiv",
    "metadata": {
        "version": "0.1.1",
        "worker": "fe75ddba",
        "model": "readerbench/ro-offense",
        "device": "cuda",
        "packages": [
            "fastapi                   0.108.0",
            "tokenizers                0.15.0",
            "torch                     2.1.2",
            "transformers              4.36.2"
        ],
        "elapsed_time": 0.0619,
        "average_time": 0.1004
    }
}
```

