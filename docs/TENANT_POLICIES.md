# Tenant-specific Policies

- Set: `POST /v1/admin/tenants/{tenant}/policy` with JSON body matching schema.
- Clear: `DELETE /v1/admin/tenants/{tenant}/policy`.
- Runtime uses `{AEGIS_POLICY_DIR}/tenants/<tenant>.yaml` if present.
