FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=120 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

WORKDIR /app
USER root

RUN groupadd -r app && useradd --no-log-init -r -g app app || true \
    && chown -R app /app \
    && mkdir -p /home/app && chown -R app /home/app

RUN pip install --no-cache-dir \
    "mlflow>=2.11,<2.12" \
    "psycopg2-binary>=2.9.9,<3" \
    "gevent>=23.9.1,<25" \
    "boto3>=1.24.28,<1.25" \
    "setuptools>=81,<82"

USER app
ENTRYPOINT []
CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "8080"]
