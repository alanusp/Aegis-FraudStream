# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env python
import os, json, time
import httpx
from sqlalchemy import create_engine, text

def main():
    url = os.getenv("AEGIS_DB_URL")
    if not url:
        raise SystemExit("AEGIS_DB_URL not set")
    eng = create_engine(url, future=True)
    with eng.connect() as c:
        rows = c.execute(text("SELECT id, callback_url, body, headers, attempts FROM webhook_failures ORDER BY id LIMIT 100")).fetchall()
        for r in rows:
            try:
                headers = json.loads(r.headers) if isinstance(r.headers, str) else {}
            except Exception:
                headers = {}
            try:
                resp = httpx.post(r.callback_url, content=r.body.encode(), headers=headers, timeout=5.0)
                if resp.status_code < 500:
                    c.execute(text("DELETE FROM webhook_failures WHERE id=:id"), { "id": r.id })
                    c.commit()
                    continue
            except Exception as e:
                pass
            c.execute(text("UPDATE webhook_failures SET attempts = attempts + 1 WHERE id=:id"), { "id": r.id })
            c.commit()

if __name__ == "__main__":
    main()
