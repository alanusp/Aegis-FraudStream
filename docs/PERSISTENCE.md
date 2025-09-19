# Persistence

- Optional database via `AEGIS_DB_URL` (e.g., `sqlite:///aegis.db` or Postgres URL).
- On startup, a `decision_logs` table is created to store decisions from `/v1/decision`.
- Disable by leaving `AEGIS_DB_URL` unset.
