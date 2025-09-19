# Secrets Management with SOPS (Guide)

- Configure `.sops.yaml` with your **age** public key.
- Encrypt: `sops -e .env > secrets/.env.enc`  Decrypt: `sops -d secrets/.env.enc > .env`.
- Do not commit plaintext secrets.
