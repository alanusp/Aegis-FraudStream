# Security Design
- Auth: API Key or JWT/JWKS with `aud`/`iss` checks.
- OPA PDP via HTTP with short backoff. Fail-open documented.
- Headers: X-Content-Type-Options, X-Frame-Options, Referrer-Policy, CSP, CORP/COOP.
- Rate limit per tenant. Idempotency support.
- Supply chain: cosign, SLSA, Trivy, OSV, gitleaks, CodeQL.
