# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env bash
set -euo pipefail
BASE="${1:-http://127.0.0.1:8080}"
curl -sf "$BASE/version" | jq . >/dev/null
curl -sf -H "Content-Type: application/json" -d '{"user_id":"u1","amount":1,"tx_count_1h":0,"country_risk":0.1}' "$BASE/v1/inference" >/dev/null
echo "Smoke OK"
