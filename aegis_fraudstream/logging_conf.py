# SPDX-License-Identifier: Apache-2.0
import logging, json, sys, time

class JsonFormatter(logging.Formatter):
    def format(self, record):
        obj = {
            "ts": int(time.time()*1000),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if hasattr(record, "rid"):
            obj["rid"] = record.rid
        return json.dumps(obj, ensure_ascii=False)

def configure_json_logging(level: str = "INFO"):
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(h)
    root.setLevel(level)
