# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env python
import json, sys, math
from collections import defaultdict

def bucket(x: float) -> str:
    if x is None: return "unknown"
    if x < 0.2: return "very_low"
    if x < 0.4: return "low"
    if x < 0.6: return "medium"
    if x < 0.8: return "high"
    return "very_high"

def main(path: str):
    # input: NDJSON decisions with fields: decision, score, features including country_risk
    counts = defaultdict(lambda: {"approve":0,"review":0,"block":0,"n":0})
    with open(path,"r",encoding="utf-8") as f:
        for line in f:
            if not line.strip(): continue
            d = json.loads(line)
            g = bucket((d.get("features") or {}).get("country_risk", 0.0))
            counts[g]["n"] += 1
            counts[g][d.get("decision","review")] += 1
    print(json.dumps(counts, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: fairness_report.py decisions.ndjson"); sys.exit(2)
    main(sys.argv[1])
