# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 Aegis FraudStream Authors

import json, secrets
from typing import Optional
import typer, uuid, httpx
from .config import settings

app = typer.Typer(help="Aegis FraudStream CLI.")

@app.command()
def version() -> None:
    print(f"Aegis FraudStream 1.3.0 | env={settings.env}")

@app.command()
def config(show_all: bool = typer.Option(False, help="Show all fields")) -> None:
    data = settings.model_dump()
    if not show_all and "redis_url" in data:
        data["redis_url"] = "redacted" if data["redis_url"] else None
    print(json.dumps(data, indent=2))

@app.command()
def openapi(out: Optional[str] = typer.Option(None, help="Write OpenAPI JSON to file")) -> None:
    from aegis_fraudstream.app import app as _app
    js = json.dumps(_app.openapi(), indent=2)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(js)
        print(f"Wrote {out}")
    else:
        print(js)

@app.command()
def gen_api_key() -> None:
    print(secrets.token_urlsafe(48))

@app.command()
def bench(url: str = "http://localhost:8080", n: int = 20) -> None:
    with httpx.Client(base_url=url, timeout=2.0, headers={"Accept":"application/vnd.aegis.v1+json"}) as c:
        for i in range(n):
            payload={"user_id":f"u-{i}","amount":i+1,"tx_count_1h":i%5,"country_risk":0.1}
            r = c.post("/v1/inference", json=payload, headers={"Idempotency-Key": str(uuid.uuid4())})
            print(i, r.status_code)

import typer, json, httpx, time, hmac, hashlib, base64
cli = typer.Typer()

def _sign(method: str, path: str, body: str, key: str) -> tuple[str,str]:
    ts = str(int(time.time()))
    msg = f"{method}\n{path}\n{body}\n{ts}".encode()
    sig = base64.b64encode(hmac.new(key.encode(), msg, hashlib.sha256).digest()).decode()
    return sig, ts

@cli.command()
def batch(file: str, base: str = "http://localhost:8080", hmac_key: str | None = None):
    """Send a JSON file with {"events":[...]}."""
    body = Path(file).read_text(encoding="utf-8")
    path = "/v1/batch"
    headers = {"content-type":"application/json"}
    if hmac_key:
        sig, ts = _sign("POST", path, body, hmac_key)
        headers["X-Signature"], headers["X-Timestamp"] = sig, ts
    with httpx.Client(timeout=10.0) as c:
        r = c.post(base+path, content=body, headers=headers)
        print(r.status_code)
        print(r.text)

@cli.command()
def batch_ndjson(file: str, base: str = "http://localhost:8080", hmac_key: str | None = None):
    """Send NDJSON file of events."""
    path = "/v1/batch/ndjson"
    headers = {"content-type":"application/x-ndjson"}
    content = Path(file).read_bytes()
    if hmac_key:
        sig, ts = _sign("POST", path, content.decode(), hmac_key)
        headers["X-Signature"], headers["X-Timestamp"] = sig, ts
    with httpx.Client(timeout=None) as c:
        with c.stream("POST", base+path, content=content, headers=headers) as r:
            print(r.status_code)
            for chunk in r.iter_bytes():
                if chunk:
                    print(chunk.decode().rstrip())

@cli.command()
def jobs_submit(file: str, base: str = "http://localhost:8080", hmac_key: str | None = None, callback: str | None = None):
    import json, httpx, time, base64, hmac, hashlib
    body = Path(file).read_text(encoding="utf-8")
    path = "/v1/jobs" + (f"?callback={callback}" if callback else "")
    headers = {"content-type":"application/json"}
    if hmac_key:
        ts = str(int(time.time()))
        sig = base64.b64encode(hmac.new(hmac_key.encode(), f"POST\n{path}\n{body}\n{ts}".encode(), hashlib.sha256).digest()).decode()
        headers["X-Signature"] = sig; headers["X-Timestamp"] = ts
    r = httpx.post(base+path, content=body, headers=headers)
    print(r.status_code, r.text)

@cli.command()
def jobs_get(job_id: str, base: str = "http://localhost:8080"):
    import httpx
    r = httpx.get(f"{base}/v1/jobs/{job_id}")
    print(r.status_code, r.text)

@cli.command()
def sign(method: str, path: str, body_file: str, hmac_key: str):
    import time, base64, hmac, hashlib
    body = Path(body_file).read_text(encoding="utf-8")
    ts = str(int(time.time()))
    sig = base64.b64encode(hmac.new(hmac_key.encode(), f"{method}\n{path}\n{body}\n{ts}".encode(), hashlib.sha256).digest()).decode()
    print(sig, ts)

@cli.command()
def sign_with_key(method: str, path: str, body_file: str, key_id: str, secret: str):
    import time, base64, hmac, hashlib
    body = Path(body_file).read_text(encoding="utf-8")
    ts = str(int(time.time()))
    sig = base64.b64encode(hmac.new(secret.encode(), f"{method}\n{path}\n{body}\n{ts}".encode(), hashlib.sha256).digest()).decode()
    print("X-Key-Id:", key_id)
    print("X-Signature:", sig)
    print("X-Timestamp:", ts)

@cli.command()
def create_api_key(tenant: str, scopes: str = "decision,metrics", rate_limit_rpm_override: int | None = None):
    from aegis_fraudstream.storage import create_api_key
    pfx, token = create_api_key(tenant, scopes, rate_limit_rpm_override)
    print({"key_prefix": pfx, "api_key": token})
