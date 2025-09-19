# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env bash
set -euo pipefail
pip install pip-licenses
pip-licenses --from=mixed --format=markdown --with-urls --with-license-file --no-license-path   --output-file THIRD_PARTY_NOTICES.md
echo "Wrote THIRD_PARTY_NOTICES.md"
