# Data Subject Requests (DSR)

- **Block processing**: `POST /v1/admin/dsr/block` `{ "user_id": "..." }` adds a salted hash to `pii_blocklist`.New inferences for that user return `review` with reason `dsr_blocklist`.
- **Status**: `GET /v1/admin/dsr/status?user_id=...` lists recorded requests.
- **Export**: `GET /v1/admin/dsr/export?user_id=...` returns pseudonymized decisions and a `user_hash` for correlation.

Notes: Audit chain remains immutable for compliance. Use `AEGIS_DSR_SALT` to control hashing.
