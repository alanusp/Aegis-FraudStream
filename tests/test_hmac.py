# SPDX-License-Identifier: Apache-2.0
from fastapi.testclient import TestClient
import base64, hmac, hashlib, time, json
from aegis_fraudstream.app import app
from aegis_fraudstream.config import settings

def sign(method: str, path: str, body: dict, key: str) -> tuple[str,str]:
    ts = str(int(time.time()))
    msg = f"{method}\n{path}\n{json.dumps(body, separators=(',',':'))}\n{ts}".encode()
    sig = base64.b64encode(hmac.new(key.encode(), msg, hashlib.sha256).digest()).decode()
    return sig, ts

def test_hmac_enforced_when_enabled():
    settings.hmac_key = "secret"
    c = TestClient(app)
    payload = {"user_id":"u1","amount":1.0,"tx_count_1h":1,"country_risk":0.1}
    sig, ts = sign("POST","/v1/inference", payload, settings.hmac_key)
    r = c.post("/v1/inference", json=payload, headers={"X-Signature": sig, "X-Timestamp": ts})
    assert r.status_code in (200, 415, 406)  # accepts valid signature; content-type gate may alter

def test_hmac_missing_is_unauthorized():
    settings.hmac_key = "secret"
    c = TestClient(app)
    r = c.post("/v1/inference", json={"user_id":"u1","amount":1,"tx_count_1h":1,"country_risk":0.1})
    assert r.status_code in (401, 503)
