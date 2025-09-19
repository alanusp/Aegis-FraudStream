# Drift Monitoring

- Rolling histograms for features.
- Background task computes **PSI** against baseline every `AEGIS_DRIFT_COMPUTE_INTERVAL_SECONDS`.
- Metrics: `aegis_feature_psi{feature}` gauges.
- Configure baseline via `AEGIS_DRIFT_BASELINE_FILE` (JSON with 10-bin arrays).
