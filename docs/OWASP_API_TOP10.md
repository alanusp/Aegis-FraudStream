# OWASP API Top 10 Mapping (extract)

- API1 Broken Object Level Authorization: OPA examples, rate limits.
- API2 Broken Auth: JWT/API key guidance, rotation.
- API3 Excessive Data Exposure: minimal schemas, no PII by default.
- API4 Lack of Resources & Rate Limiting: token bucket + HPA.
- API5 Broken Function Level Authorization: admin endpoints separated + OPA.
- API7 Security Misconfiguration: headers, non-root, seccomp, Kyverno.
- API8 Injection: pydantic validation and parametrization.
- API10 SSRF: no outbound fetches by default; allowlist if added.
