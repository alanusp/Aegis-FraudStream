# API
- `POST /v1/inference` → score + features
- `POST /v1/inference/explain` → reason codes
- `POST /v1/inference/stream` → SSE
- `POST /v1/inference/batch`
- `GET /v1/schemas`
- `GET /metrics`, `GET /health`, `GET /ready`
- Admin: `POST /admin/maintenance` with header `X-Admin-Token: <token>`
Accept: `application/json` or `application/vnd.aegis.v1+json`.
