# Threat Model (STRIDE + DFD)

## Data Flow
- Client -> API `/v1/score` (TLS)
- API -> Policy Engine
- API -> Model -> Storage (optional features)
- API -> Metrics/Logs

## STRIDE Summary
- Spoofing: JWT/HMAC auth options documented; admin endpoints gated.
- Tampering: Request ID + idempotency + structured logs, SBOM and signatures.
- Repudiation: Audit trail; request/decision correlation IDs.
- Information Disclosure: PII off by default; classification per DATA_CLASSIFICATION.md.
- Denial of Service: Rate limiting + quotas; body size limits; gzip optional.
- Elevation of Privilege: Least-privilege containers; non-root; RBAC for K8s.
