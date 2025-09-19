# Async Jobs

- `POST /v1/jobs` accepts `BatchRequest` and enqueues work.
- `GET /v1/jobs/{job_id}` returns `{"status":"queued|done","results":[...]}`.
- Backed by in-process worker; swap to Redis/RQ externally if needed.
