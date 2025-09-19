# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env bash
set -euo pipefail
pip install scalene
scalene -m uvicorn aegis_fraudstream.app:app --port 8080 --duration 15
