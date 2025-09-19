# SLOs and Error Budgets

- Availability SLO: 99.9% monthly.
- P99 latency SLO: ≤ 150 ms on `/v1/score` at 100 RPS baseline.
- Error budget policy: Freeze deploys if budget exhausted; rollback then fix-forward.
