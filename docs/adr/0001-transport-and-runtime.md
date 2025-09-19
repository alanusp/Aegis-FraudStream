# ADR 0001: Transport and Runtime

- Status: Accepted
- Context: API needs efficient JSON and secure transport.
- Decision: Use FastAPI with ORJSON; uvicorn default, Hypercorn for HTTP/2 where TLS is required.
- Consequences: Lower latency JSON, HTTP/2 support for modern clients.
