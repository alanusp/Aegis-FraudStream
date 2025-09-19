# Deploy Checklist

- [ ] CI green across lint, type, tests, SAST, DAST, IaC scans, licenses.
- [ ] Image signed and SBOM attested. Cosign verify passes.
- [ ] Kyverno and Gatekeeper policies applied in cluster.
- [ ] HPA and PDB configured per expected traffic.
- [ ] Alerts loaded: error rate and latency burn rates.
- [ ] SLOs reviewed and dashboards linked.
- [ ] Secrets provisioned via ExternalSecrets or SOPS.
- [ ] Rollout strategy defined (Argo canary with AnalysisTemplate).
