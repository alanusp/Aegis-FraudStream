# syntax=docker/dockerfile:1.7
FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1 SOURCE_DATE_EPOCH=315532800 PYTHONHASHSEED=0
WORKDIR /app
LABEL org.opencontainers.image.title="Aegis FraudStream" \
      org.opencontainers.image.source="https://github.com/your-org/aegis-fraudstream" \
      org.opencontainers.image.licenses="Apache-2.0"

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends             build-essential curl ca-certificates tini &&             rm -rf /var/lib/apt/lists/*

# Use uv for fast installs
RUN pip install --no-cache-dir uv==0.4.24

# Copy project files
COPY pyproject.toml README.md LICENSE .
COPY aegis_fraudstream ./aegis_fraudstream
COPY examples ./examples

# Install runtime deps only
RUN uv pip install --system --compile --no-cache .

# Non-root user
RUN useradd -r -u 10001 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080
ENTRYPOINT ["/usr/bin/tini","--"]
CMD ["uvicorn","aegis_fraudstream.app:app","--host","0.0.0.0","--port","8080"]

HEALTHCHECK --interval=30s --timeout=3s --retries=5 CMD curl -fsS http://127.0.0.1:8080/health || exit 1
