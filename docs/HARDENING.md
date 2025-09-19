# Hardening Guide

- Run Distroless, non-root, read-only root FS, seccomp and AppArmor.
- Set `AEGIS_ALLOWED_HOSTS`, `AEGIS_ADMIN_TOKEN`, `AEGIS_RESPONSE_SIGNING_KEY`.
- Enforce TLS 1.2+ at the ingress. Prefer mTLS for admin.
- Configure Redis and Postgres with auth and network segmentation.
