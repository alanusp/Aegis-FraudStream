# Database Indexes

- `ix_decision_logs_user_created(user_id, created_at)` for export-by-user.
- `ix_decision_logs_created(created_at)` for retention sweeps.
- `ix_decision_logs_tenant_created(tenant, created_at)` for multitenant analytics.
