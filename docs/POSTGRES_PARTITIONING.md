# PostgreSQL Partitioning (Guide)

- Prefer monthly partitions on `decision_logs(created_at)` under high write volumes.
- Create partitions and attach with CHECK constraints, and a BEFORE INSERT trigger to route by month.
- Handle retention by detaching and dropping old partitions.
