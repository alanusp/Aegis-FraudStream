# Security Architecture

- Boundary: FastAPI service with non-root container, hardened Helm (Seccomp/AppArmor), NetworkPolicy.
- Supply chain: SBOM, SLSA provenance, Scorecards, Dependabot, REUSE, license notices.
- App: security headers, optional rate limiting, CORS control, metrics opt-in, OTel opt-in.
- Data: classification, retention, encryption docs; incident response and fairness evaluation.
