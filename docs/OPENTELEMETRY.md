# OpenTelemetry

- Install extras: `pip install .[otel]`
- Set `OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318/v1/traces`
- Traces include FastAPI spans via native instrumentation.
