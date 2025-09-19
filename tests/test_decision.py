# SPDX-License-Identifier: Apache-2.0
from fastapi.testclient import TestClient
from aegis_fraudstream.app import app

def test_decision_endpoint():
    c = TestClient(app)
    r = c.post("/v1/decision", json={"user_id":"u1","amount":100,"tx_count_1h":0,"country_risk":0.1})
    assert r.status_code == 200
    d = r.json()
    assert "decision" in d and "score" in d
