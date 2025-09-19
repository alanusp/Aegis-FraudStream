# Multi-tenancy & Quotas

- Enable via `tenant_mode=true` and `allowed_tenants` list.
- Per-tenant RPM rate limit with Redis.
- Per-tenant **daily quota** with key `quota:{tenant}:{YYYY-MM-DD}`.
- Required header: `X-Tenant-ID`.
