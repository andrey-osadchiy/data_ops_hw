# Homework 24 — Full ML service

## What is inside
- `research/train.ipynb` — notebook for training, logging and registering the model in MLflow
- `mlapp/server.py` — FastAPI service with `/api/v1/predict`
- `mlapp/__main__.py` — service entrypoint
- `Dockerfile` — image for the service
- `docker-compose.yaml` — local launch of the service
- `model/diabets_model.pkl` — local downloaded model placeholder (generate from notebook)

## Run locally
```bash
pip install -r requirements.txt
python -m mlapp
```

## Test
```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"age":59.0,"sex":2.0,"bmi":32.1,"bp":101.0,"s1":157.0,"s2":93.2,"s3":38.0,"s4":4.0,"s5":4.8598,"s6":87.0}'
```
