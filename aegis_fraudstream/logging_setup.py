# SPDX-License-Identifier: Apache-2.0
import os, json, logging, sys, time

class _JsonFormatter(logging.Formatter):
    def format(self, record):
        d = {
            "ts": int(time.time()*1000),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        for k in ("request_id","tenant"):
            v = getattr(record, k, None)
            if v: d[k] = v
        return json.dumps(d, ensure_ascii=False)
def configure_logging():
    if os.getenv("AEGIS_LOG_JSON","").lower() not in ("1","true","yes"):
        return
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(_JsonFormatter())
    root.addHandler(h)
    root.setLevel(getattr(logging, os.getenv("AEGIS_LOG_LEVEL","INFO").upper(), logging.INFO))
