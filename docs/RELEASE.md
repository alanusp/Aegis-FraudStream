# Release Process

1. Merge to `main` with Conventional Commits.
2. Tag `vX.Y.Z`. GitHub Action builds image and signs with Cosign. SLSA provenance runs on tag.
3. Generate `requirements.lock` via lock workflow for reproducible installs.
4. Publish docs via MkDocs Pages.
