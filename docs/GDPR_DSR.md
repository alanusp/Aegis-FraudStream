# Data Subject Requests

Admin-only endpoints (require `X-Admin-Token`):
- `GET /v1/admin/decisions/export?user_id=...` returns NDJSON of decisions.
- `DELETE /v1/admin/decisions/{user_id}` hard-deletes stored decisions.
Requires `AEGIS_DB_URL` configured.
