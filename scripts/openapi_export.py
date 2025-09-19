# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env python
import sys, json
from aegis_fraudstream.app import app

def main(path: str = "openapi.json"):
    data = app.openapi()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(path)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv)>1 else "openapi.json")
