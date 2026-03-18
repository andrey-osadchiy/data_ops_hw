FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=on

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY mlapp ./mlapp
COPY model ./model

EXPOSE 8000

CMD ["python", "-m", "mlapp"]
