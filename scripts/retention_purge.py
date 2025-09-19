# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env python
from __future__ import annotations
import os, sys
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

def main(days: int = 90):
    url = os.getenv("AEGIS_DB_URL")
    if not url:
        print("AEGIS_DB_URL not set", file=sys.stderr); return 2
    engine = create_engine(url, future=True)
    cutoff = datetime.utcnow() - timedelta(days=days)
    with engine.begin() as c:
        res = c.execute(text("DELETE FROM decision_logs WHERE created_at < :cutoff"), {"cutoff": cutoff})
        print({"deleted": res.rowcount or 0, "cutoff": cutoff.isoformat()})
    return 0

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=90)
    args = ap.parse_args()
    raise SystemExit(main(args.days))
