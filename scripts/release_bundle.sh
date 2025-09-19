# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env bash
set -euo pipefail
rm -rf build dist || true
python -m build
./scripts/sbom_python.sh
sha256sum dist/* sbom-python.cdx.json > RELEASE_SHA256SUMS.txt
echo "Bundle ready: dist/*, sbom-python.cdx.json, RELEASE_SHA256SUMS.txt"
