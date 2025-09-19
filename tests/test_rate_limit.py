# SPDX-License-Identifier: Apache-2.0
import time
from fastapi.testclient import TestClient
from aegis_fraudstream.app import app
from aegis_fraudstream.config import settings

def test_rate_limit_in_memory():
    settings.rate_limit_rpm = 2
    c = TestClient(app)
    payload = {"user_id":"u1","amount":1,"tx_count_1h":1,"country_risk":0.1}
    r1 = c.post("/v1/inference", json=payload)
    r2 = c.post("/v1/inference", json=payload)
    r3 = c.post("/v1/inference", json=payload)
    assert r3.status_code in (429, 503)
