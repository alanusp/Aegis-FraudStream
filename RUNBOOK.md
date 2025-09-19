# SRE Runbook

## Detect
- Alerts: 5xx rate, p95 latency, Redis errors, rate-limit saturation.

## Diagnose
- Check `/health` and `/ready`. Inspect recent deploy and Redis connectivity.
- View Grafana dashboard and logs with request IDs.

## Mitigate
- Toggle maintenance `/admin/maintenance` with authz.
- Scale via HPA values. Roll back to previous image tag.

## Postmortem
- Open incident doc, add action items to ROADMAP.
