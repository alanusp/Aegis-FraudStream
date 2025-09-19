# Policy Engine

- File format: YAML (`policy/default.policy.yaml`).
- Fields: `if` (Python boolean over `score`), `decision` in {approve, review, block}, `reason` string.
- Endpoint: `POST /v1/decision` returns score, decision, reason, explanation, policy_version.
- Configure custom policy via `AEGIS_POLICY_FILE`.
