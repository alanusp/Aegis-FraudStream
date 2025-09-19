# Policy Admin API

- `POST /v1/admin/policy` with JSON body matching schema writes an override file and hot-reloads cache.
- `DELETE /v1/admin/policy` clears override and reloads default policy.
- Decision responses now include `policy_checksum` for provenance.
