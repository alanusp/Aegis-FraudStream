# SLOs and Error Budgets

- Availability SLO: 99.9% monthly.
- Latency SLO: p95 inference < 200ms during 99% of 5m windows.
- Error budget policy: if budget burn > 2x over 1h, freeze deploys until mitigated.
