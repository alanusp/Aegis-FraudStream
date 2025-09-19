# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env python
import os, json, hashlib
from sqlalchemy import create_engine, text as T

def main(limit=100000):
    url = os.getenv("AEGIS_DB_URL","sqlite:///aegis.db")
    eng = create_engine(url, future=True)
    with eng.connect() as c:
        rows = c.execute(T("SELECT id, user_id, decision, reason, score, created_at, tenant, chain_hash FROM decision_logs ORDER BY id ASC LIMIT :lim"), {"lim": limit}).fetchall()
    prev = b""; ok = True; last = None
    for r in rows:
        payload = json.dumps({"user_id": r.user_id, "decision": r.decision, "reason": r.reason, "score": float(r.score), "created_at": str(r.created_at), "tenant": getattr(r, "tenant", None)}, sort_keys=True).encode()
        calc = hashlib.sha256(prev + payload).hexdigest()
        if r.chain_hash != calc:
            ok = False; break
        prev = calc.encode(); last = calc
    print(json.dumps({"ok": ok, "last_hash": last, "checked": len(rows)}))

if __name__ == "__main__":
    import sys
    main(int(sys.argv[1]) if len(sys.argv)>1 else 100000)
