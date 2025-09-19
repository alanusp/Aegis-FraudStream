# Idempotency

- Send header `Idempotency-Key` on mutating requests.
- Duplicate within TTL returns **409** without reprocessing. TTL default 600s, override via `X-Idempotency-TTL`.
- Uses Redis when available or in-memory fallback.
