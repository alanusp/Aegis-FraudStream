# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env bash
set -euo pipefail
# Usage: PGURL='postgresql://user:pass@host:5432/db' ./scripts/pg_backup.sh
: "${PGURL:?set PGURL}"
ts=$(date +%Y%m%d-%H%M%S)
out="backups/pg-${ts}.dump"
mkdir -p backups
pg_dump "$PGURL" > "$out"
echo "$out"
