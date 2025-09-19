# OWASP API Security Top 10 Mapping

- API1: Broken Object Level Authorization → scopes + tenant isolation + RLS.
- API2: Broken Authentication → OIDC + API key hashing, admin token.
- API4: Unrestricted Resource Consumption → rate limits, quotas, body size and concurrency caps.
- API6: Unrestricted Access to Sensitive Business Flows → admin scope, maintenance + read-only + freeze modes.
- API7: Server Side Request Forgery → webhook allowlist + circuit breaker.
- API8: Security Misconfiguration → hardened Dockerfile, security headers, allowed hosts, K8s securityContext.
- API9: Improper Inventory → OpenAPI export, Spectral lint, Postman collection.
- API10: Unsafe Consumption → HTTP client timeouts, allowlists.
