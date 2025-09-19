# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
import typer, json, httpx, os, time, hmac, hashlib, base64
app = typer.Typer(help="Aegis FraudStream CLI")

def _sign(method: str, path: str, body: str, key: str) -> tuple[str,str]:
    ts = str(int(time.time()))
    msg = f"{method}\n{path}\n{body}\n{ts}".encode()
    sig = base64.b64encode(hmac.new(key.encode(), msg, hashlib.sha256).digest()).decode()
    return sig, ts

@app.command()
def infer(base: str = typer.Option("http://localhost:8080", help="Base URL"),
          user_id: str = "u1",
          amount: float = 10.0,
          tx_count_1h: int = 1,
          country_risk: float = 0.1,
          hmac_key: str = typer.Option(None, help="Optional HMAC key")):
    path = "/v1/inference"
    payload = {"user_id": user_id, "amount": amount, "tx_count_1h": tx_count_1h, "country_risk": country_risk}
    body = json.dumps(payload, separators=(',',':'))
    headers = {"content-type":"application/json"}
    if hmac_key:
        sig, ts = _sign("POST", path, body, hmac_key)
        headers["X-Signature"], headers["X-Timestamp"] = sig, ts
    with httpx.Client(timeout=5.0) as c:
        r = c.post(base + path, content=body, headers=headers)
        typer.echo(r.status_code)
        typer.echo(r.text)

if __name__ == "__main__":
    app()
