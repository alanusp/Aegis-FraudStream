# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env python
import os, json
from sqlalchemy import create_engine, text
try:
    import pandas as pd
except Exception as e:
    raise SystemExit("pandas required")
try:
    import pyarrow as pa, pyarrow.parquet as pq  # type: ignore
except Exception:
    raise SystemExit("pyarrow required")

def main(out="export/decision_logs.parquet"):
    url = os.getenv("AEGIS_DB_URL","sqlite:///aegis.db")
    eng = create_engine(url, future=True)
    with eng.connect() as c:
        rows = c.execute(text("SELECT user_id, decision, reason, score, created_at FROM decision_logs ORDER BY created_at")).fetchall()
    df = pd.DataFrame(rows, columns=["user_id","decision","reason","score","created_at"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, out)
    print(out)

if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv)>1 else "export/decision_logs.parquet")
