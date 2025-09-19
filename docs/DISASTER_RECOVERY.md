# Disaster Recovery

- Backups: use `scripts/pg_backup.sh` daily; store offsite with 30-day retention.
- Restore: provision empty DB, apply Alembic, then restore dumps.
- Keys: rotate with `scripts/rotate_data_key.py`.
