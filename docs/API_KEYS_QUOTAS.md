# API Key Quotas

- Optional monthly quotas per API key. Set during creation (`monthly_quota` integer) or update via DB.
- Enforcement requires Redis. Keys counted under `akq:<prefix>:YYYYMM`.
- Check usage: `GET /v1/admin/apikeys/{prefix}/usage` with `X-Admin-Token`.
