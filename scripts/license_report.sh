# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env bash
set -euo pipefail
pip install pip-licenses
pip-licenses --format=csv --with-urls --with-license-file --output-file third_party_licenses.csv
echo "Wrote third_party_licenses.csv"
