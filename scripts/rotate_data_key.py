# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env python
import os, json
from sqlalchemy import create_engine, text
from cryptography.fernet import Fernet

def main():
    url = os.getenv("AEGIS_DB_URL")
    old = os.getenv("AEGIS_DATA_KEY")
    new = os.getenv("AEGIS_DATA_KEY_NEW")
    if not (url and old and new):
        raise SystemExit("set AEGIS_DB_URL, AEGIS_DATA_KEY, AEGIS_DATA_KEY_NEW")
    f_old, f_new = Fernet(old.encode()), Fernet(new.encode())
    eng = create_engine(url, future=True)
    with eng.begin() as c:
        rows = c.execute(text("SELECT id, features, features_cipher FROM decision_logs WHERE features_cipher IS NOT NULL")).fetchall()
        for r in rows:
            try:
                raw = f_old.decrypt(r.features_cipher.encode())
                token = f_new.encrypt(raw).decode()
                c.execute(text("UPDATE decision_logs SET features_cipher=:t WHERE id=:i"), {"t": token, "i": r.id})
            except Exception:
                pass
    print("rotation complete")

if __name__ == "__main__":
    main()
