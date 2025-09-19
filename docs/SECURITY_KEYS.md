# HMAC Key Rotation

- Configure multiple keys via `AEGIS_HMAC_KEYS='{"key1":"secret1","key2":"secret2"}'` and `AEGIS_HMAC_ACTIVE_KEY_ID=key2`.
- Clients send headers `X-Key-Id`, `X-Signature`, `X-Timestamp`.
- Old keys remain valid during rotation; server tries all.
