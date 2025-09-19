# PCI DSS Considerations (Non-scoping Guidance)

- No PAN storage by default; redaction and encryption hooks exist.
- Enforce TLS 1.2+ and mTLS at the edge (see `ops/nginx-mtls.conf`).
- Use tokenization upstream; treat this service as out-of-scope where possible.
