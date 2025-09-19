# Distributed Jobs

JobManager uses a Redis-backed lock (`jobs-lock`) to run exactly-once background tasks per cluster.
