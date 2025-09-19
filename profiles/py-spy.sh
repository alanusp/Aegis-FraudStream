# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env bash
set -euo pipefail
pip install py-spy
uvicorn aegis_fraudstream.app:app --port 8080 &
PID=$!
sleep 1
py-spy record -o profile.svg --pid $PID --rate 200 --duration 15
kill $PID || true
echo "Wrote profiles/profile.svg"
