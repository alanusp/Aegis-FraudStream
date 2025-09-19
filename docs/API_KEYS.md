# API Keys

- Create: `POST /v1/admin/apikeys` with `X-Admin-Token` or CLI `aegis create-api-key --tenant TENANT`.
- Authenticate by header `X-API-Key`. The service derives tenant, scopes, and optional per-key rate limit.
- Keys are stored hashed with SHA-256 plus server-side pepper. Only prefixes are queryable; raw key is shown once.
