# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env bash
set -euo pipefail
pip install sigstore
for f in dist/*; do
  echo "Verifying $f"
  python -m sigstore verify identity --cert-oidc-issuer https://token.actions.githubusercontent.com --cert-identity-regexp '.*' "$f"
done
