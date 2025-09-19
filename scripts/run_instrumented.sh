# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env bash
set -euo pipefail
export OTEL_TRACES_EXPORTER=${OTEL_TRACES_EXPORTER:-otlp}
export OTEL_METRICS_EXPORTER=${OTEL_METRICS_EXPORTER:-otlp}
export OTEL_EXPORTER_OTLP_ENDPOINT=${OTEL_EXPORTER_OTLP_ENDPOINT:-http://127.0.0.1:4318}
opentelemetry-instrument uvicorn aegis_fraudstream.app:app --host 0.0.0.0 --port 8080
