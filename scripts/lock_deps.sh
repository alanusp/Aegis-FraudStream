# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env bash
set -euo pipefail
pip install pip-tools
pip-compile --resolver=backtracking --generate-hashes -o requirements.txt requirements.in
echo "Wrote requirements.txt"
