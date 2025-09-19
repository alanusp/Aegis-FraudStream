# Response Signing

- Enable with `AEGIS_RESPONSE_SIGNING_KEY`.
- Every HTTP response gets `X-Response-Signature` with base64(HMAC-SHA256(body)).
- Clients can verify integrity and provenance.
