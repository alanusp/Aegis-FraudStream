# SPDX-License-Identifier: Apache-2.0
# Build stage
FROM python:3.11-slim AS build
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=off PIP_DISABLE_PIP_VERSION_CHECK=on
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml README.md LICENSE .
COPY aegis_fraudstream ./aegis_fraudstream
COPY aegis_client ./aegis_client
RUN pip install --upgrade build && python -m build

# Runtime stage
FROM python:3.11-slim
RUN useradd -r -u 10001 -g users aegis
WORKDIR /app
COPY --from=build /app/dist/*.whl /tmp/
RUN pip install /tmp/*.whl && rm -rf /root/.cache/pip
EXPOSE 8080
ENV AEGIS_ENV=production
USER 10001
ENTRYPOINT ["uvicorn","aegis_fraudstream.app:app","--host","0.0.0.0","--port","8080"]

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s CMD wget -qO- http://127.0.0.1:8080/health || exit 1
