# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env python
import os, sys
REQUIRED = ["AEGIS_LOG_LEVEL"]
WARN = ["AEGIS_DB_URL","AEGIS_REDIS_URL"]
missing = [k for k in REQUIRED if not os.getenv(k)]
if missing:
    print("Missing required env:", ", ".join(missing)); sys.exit(2)
for k in WARN:
    if not os.getenv(k):
        print("Warning: not set", k)
print("OK")
