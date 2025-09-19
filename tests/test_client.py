# SPDX-License-Identifier: Apache-2.0
from aegis_fraudstream.client import AegisClient, ClientConfig
from aegis_fraudstream.schemas import Event
from aegis_fraudstream.app import app
from fastapi.testclient import TestClient

def test_client_score():
    tc = TestClient(app)
    evt = Event(user_id="u1", amount=12.34)  # type: ignore[arg-type]
    r = tc.post("/v1/score", json=evt.model_dump())
    assert r.status_code == 200
    js = r.json()
    assert "score" in js and 0.0 <= js["score"] <= 1.0
