# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env bash
set -euo pipefail
mkdir -p certs
openssl req -x509 -newkey rsa:2048 -nodes -keyout certs/dev.key -out certs/dev.crt -subj "/CN=localhost" -days 365
echo "Generated certs/dev.crt and certs/dev.key"
