# Release Process

1. Branch and land changes via PR with green CI.
2. Merge to `main` using conventional commits.
3. `release-please` opens a PR. Merge to create tag `vX.Y.Z`.
4. GitHub Actions publish wheel to PyPI and image to GHCR with SBOM + provenance.
5. Verify cosign signatures and attestations before deploy.
