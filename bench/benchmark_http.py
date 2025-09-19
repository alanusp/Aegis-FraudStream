# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
import time, statistics, httpx, json, random

def run(n=200):
    url = "http://localhost:8080/v1/inference"
    times = []
    with httpx.Client(timeout=5.0) as c:
        for _ in range(n):
            payload = {"user_id":"u1","amount":random.random()*100,"tx_count_1h":1,"country_risk":0.1}
            t0 = time.perf_counter()
            r = c.post(url, json=payload)
            r.raise_for_status()
            times.append((time.perf_counter()-t0)*1000)
    p50 = statistics.median(times)
    p95 = sorted(times)[int(0.95*len(times))-1]
    print({"count": n, "p50_ms": round(p50,2), "p95_ms": round(p95,2)})
if __name__ == "__main__":
    run()
