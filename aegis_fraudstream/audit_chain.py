# SPDX-License-Identifier: Apache-2.0
import hmac, hashlib, json, os, time, threading, pathlib

_LOCK = threading.Lock()

def _key() -> bytes:
    k = os.getenv("AEGIS_AUDIT_HMAC_KEY","").encode()
    if not k:
        # non-empty default to avoid None; encourage proper key in prod
        k = b"default-audit-key"
    return k

def _path() -> str:
    p = os.getenv("AEGIS_AUDIT_LOG","aegis_audit.log")
    return p

def append(event: dict) -> dict:
    """Append event with HMAC chain. Returns the record written."""
    now = int(time.time())
    event = dict(event)
    event.setdefault("ts", now)
    event.setdefault("type","decision")
    path = _path()
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    prev = b""
    if os.path.exists(path):
        with open(path, "rb") as f:
            try:
                last = f.readlines()[-1].decode().strip()
                prev = json.loads(last).get("sig"," ").encode()
            except Exception:
                prev = b""
    payload = json.dumps({k: event[k] for k in sorted(event)}, separators=(",", ":"), ensure_ascii=False).encode()
    msg = prev + b"|" + payload
    sig = hmac.new(_key(), msg, hashlib.sha256).hexdigest()
    record = dict(event); record["prev"] = prev.decode() if prev else ""; record["sig"] = sig
    with _LOCK:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record
