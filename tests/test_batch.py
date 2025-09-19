# SPDX-License-Identifier: Apache-2.0
from fastapi.testclient import TestClient
from aegis_fraudstream.app import app

def test_batch_scores():
    c = TestClient(app)
    payload = {"events":[{"user_id":"u1","amount":10,"tx_count_1h":2,"country_risk":0.1},
                         {"user_id":"u2","amount":20,"tx_count_1h":0,"country_risk":0.3}]}
    r = c.post("/v1/batch", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "scores" in data and len(data["scores"])==2

def test_batch_ndjson():
    c = TestClient(app)
    body = b'{"user_id":"u1","amount":10,"tx_count_1h":2,"country_risk":0.1}\n'
    r = c.post("/v1/batch/ndjson", content=body, headers={"content-type":"application/x-ndjson"})
    assert r.status_code == 200
