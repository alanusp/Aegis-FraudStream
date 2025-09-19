# Secrets with SOPS

- Install `age` and `sops`.
- Place encrypted files as `*.enc.yaml` using `.sops.yaml` rules.
- Example:
  ```bash
  export SOPS_AGE_KEY_FILE=~/.config/sops/age/keys.txt
  sops -e -i secrets/redis.enc.yaml
  ```
