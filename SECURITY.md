# Security Policy — Aegis FraudStream

## Summary
This project is security-first: least-privilege, privacy-by-default, and verifiable supply-chain. This document explains how to report vulnerabilities, what is in scope, our timelines, and how we ship fixes safely.

## Reporting a Vulnerability
Preferred channels:
- Email: alanursapu@gmail.com (maintainer: alanusp)
- GitHub: Security → “Report a vulnerability” (private advisory)
- `.well-known/security.txt` and `SECURITY_CONTACTS` in the repo

Acknowledgement SLA:
- **Within 72h**: we confirm receipt and share a tracking ID
- **Within 7 days**: triage + severity (CVSS) + provisional plan
- **Target 30 days**: fix or mitigation for High/Critical; 90 days for others

If you need encryption, request a temporary PGP key via email before sending details.

## Coordinated Disclosure
Default embargo is **90 days**. We coordinate patch availability and public disclosure. For actively exploited Critical issues, we may do an accelerated out-of-band patch and announce sooner.

## Scope (In)
- Runtime service: `aegis_fraudstream` (FastAPI app, endpoints, middlewares)
- CLI and Python client
- Helm chart and Kubernetes manifests
- Docker image and Dockerfile
- Documentation site and example configs

## Scope (Out)
- Third-party clouds or hosting not controlled by this project
- Social engineering and physical attacks
- Denial of Service that requires volumetric traffic
- Automated scanners’ low-signal issues (e.g., missing `autocomplete="off"`)
- Attacks requiring root/host compromise or non-default insecure settings

## Safe Harbor
Good-faith research following this policy will not be subject to legal action. Do not exfiltrate data, pivot to third parties, or degrade service. Use local/dev environments when possible.

## How to Report (Template)
~~~
Title: Short summary of the vulnerability
Component: e.g., /v1/score handler, Helm values, Dockerfile
Version/Commit: e.g., v1.2.3 (abc1234)
Severity: your CVSS v3.1 vector if available
PoC: exact steps with expected/actual result
Impact: data exposure, RCE, privilege, integrity
Remediation ideas: optional
Contact: how we can reach you (timezone)
~~~

## Repro and Test Guidance
Local API:
    uv pip install -e ".[dev]" --system
    uvicorn aegis_fraudstream.app:app --port 8080

Container:
    docker build -t aegis:local .
    docker run -p 8080:8080 aegis:local

Kubernetes (kind):
    make kind-up kind-deploy kind-test

Do not test DoS against shared infrastructure. Use synthetic data only.

## Severity and Triage
- Severity via **CVSS v3.1** with context (default configuration).
- CWE mapping when applicable.
- We maintain a private advisory, backport if needed, and ship a coordinated release.

## Patch, Release, and CVE
- Fixes include tests and docs; security-relevant configs default to secure.
- Release via GitHub Security Advisory; request a **CVE** through GitHub if warranted.
- Containers are published to GHCR; PyPI via Trusted Publisher OIDC.

## Hardening Summary
- Non-root containers; read-only filesystem; minimal image
- Security headers, optional rate-limit and PII redaction
- NetworkPolicy, HPA, PDB, ServiceMonitor in Helm
- Seccomp/AppArmor annotations
- HEALTHCHECK in Docker
- Optional metrics (`/metrics`) and OTel

## Dependency and Supply-Chain Controls
- SBOM (SPDX JSON) on release
- Container signing and attestations via **Sigstore Cosign (keyless)**
- CI scanners: CodeQL, Semgrep, Bandit, Safety, OSV Scanner, pip-audit
- IaC scanners: Checkov, KICS; policy checks with Conftest/OPA
- License notices with `pip-licenses`; REUSE + SPDX headers

## Privacy
By default we minimize data. See:
- `PRIVACY.md`
- `docs/DATA_CLASSIFICATION.md`
- `docs/DATA_RETENTION.md`
- `docs/DATA_ENCRYPTION.md`

## Responsible Testing Boundaries
Allowed without prior notice:
- Local and container tests
- Static analysis against this repository
- Helm/Kubernetes linting in local clusters

Require prior written consent:
- Any testing on third-party deployments
- High-traffic or stress/DoS testing
- Social engineering

## Security Contacts
- Maintainer: **alanusp** • **alanursapu@gmail.com**
- Emergency: mark the email **[URGENT]** and include a phone/IM contact for call-backs.

## Recognition
We credit reporters in release notes and `SECURITY.md` (unless you request anonymity). No monetary bounty is offered at this time.

## Related Documents
- `INCIDENT_RESPONSE.md`
- `ETHICS.md`, `FAIRNESS_EVAL.md`
- `docs/THREAT_MODEL.md`, `docs/SECURITY_ARCHITECTURE.md`
- `SLO.md`, `SOC2_MAPPING.md`, `VPAT.md`

## Supported Versions
| Version branch | Security fixes | End of support |
| --- | --- | --- |
| main | Yes | rolling |
| latest tagged (N) | Yes | when N+2 ships |
| N-1 | Critical only | when N+3 ships |

## Changelog of Security Policy
- 2025-09-19: Initial comprehensive policy adopted.

Thank you for helping keep Aegis FraudStream and its users safe.