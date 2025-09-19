# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env bash
set -euo pipefail
: "${PORT:=8080}"
: "${WEB_CONCURRENCY:=1}"
exec uvicorn aegis_fraudstream.app:app --host 0.0.0.0 --port "$PORT" --workers "$WEB_CONCURRENCY"
