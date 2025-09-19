# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env python
import os, sys, time, shutil
from urllib.parse import urlparse
def main():
    url = os.getenv("AEGIS_DB_URL","sqlite:///aegis.db")
    if url.startswith("sqlite:///"):
        path = url.replace("sqlite:///","")
        ts = time.strftime("%Y%m%d-%H%M%S")
        out = f"backups/aegis-{ts}.sqlite3"
        os.makedirs("backups", exist_ok=True)
        shutil.copy2(path, out)
        print(out)
    else:
        print("Non-sqlite backup not implemented", file=sys.stderr); sys.exit(2)
if __name__ == "__main__":
    main()
