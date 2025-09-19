# Operations Runbook

- Deploy: Helm chart `charts/aegis`. Check `/readyz` before traffic.
- Scale: HPA triggers at 70% CPU. See `hpa.yaml`.
- Alerts: import `ops/prometheus-alerts.yml`.
- Incidents: capture `X-Request-ID`, check logs by request id.
