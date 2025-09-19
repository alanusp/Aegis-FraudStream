# Container Security

- Run with `--security-opt seccomp=docker/seccomp.profile.json` and AppArmor `--security-opt apparmor=docker-default`.
- Non-root, read-only root FS, capability drop already configured in chart and Dockerfile.secure.
