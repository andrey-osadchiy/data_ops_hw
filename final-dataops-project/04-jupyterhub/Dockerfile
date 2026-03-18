FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=120 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

WORKDIR /app

# system deps + nodejs for configurable-http-proxy
RUN apt-get update --yes \
 && apt-get install -y --no-install-recommends \
      curl build-essential sqlite3 ca-certificates \
 && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
 && apt-get update --yes \
 && apt-get install -y --no-install-recommends nodejs \
 && npm install -g configurable-http-proxy \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Python deps (   : sqlalchemy<2, jupyterhub 4.x, dockerspawner)
RUN python -m pip install -U pip \
 && python -m pip install \
      "jupyterhub>=4,<5" \
      "sqlalchemy<2" \
      "dockerspawner>=14,<15"

# JupyterHub     docker-compose (    )
CMD ["jupyterhub", "--help"]
