# Docker Hardening

- Use `docker/Dockerfile.secure` for non-root + distroless runtime.
- Combine with `docker/seccomp-profile.json` and `--cap-drop=ALL --read-only` flags.
