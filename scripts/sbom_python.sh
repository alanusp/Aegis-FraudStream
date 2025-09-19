# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env bash
set -euo pipefail
pip install cyclonedx-bom
cyclonedx-py --format json --output-file sbom-python.cdx.json
echo "Wrote sbom-python.cdx.json"
