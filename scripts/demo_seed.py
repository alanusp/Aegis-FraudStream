# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env python
import os, random, time
import httpx, json

BASE = os.getenv("AEGIS_BASE","http://127.0.0.1:8080")
KEY = os.getenv("AEGIS_KEY")

def main(n=100):
    h = {"content-type":"application/json"}
    if KEY: h["X-API-Key"]=KEY
    with httpx.Client(timeout=5.0) as c:
        for i in range(n):
            body = {"user_id": f"u{i}", "amount": random.random()*100, "tx_count_1h": random.randint(0,5), "country_risk": random.random()}
            r = c.post(f"{BASE}/v1/inference", json=body, headers=h)
            print(i, r.status_code)
            time.sleep(0.05)

if __name__ == "__main__":
    import sys
    main(int(sys.argv[1]) if len(sys.argv)>1 else 100)
