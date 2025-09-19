# Runtime Hardening

- Use `docker run --security-opt seccomp=./docker/seccomp-profile.json --security-opt=no-new-privileges`.
- Combine with distroless and non-root user.
