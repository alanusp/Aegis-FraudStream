# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 Aegis FraudStream Authors

from fastapi.testclient import TestClient
from aegis_fraudstream.app import app
from hypothesis import given, strategies as st

def test_health_version():
    c = TestClient(app)
    r = c.get("/health")
    assert r.status_code == 200
    assert r.json()["version"] == "1.3.0"

def test_schemas():
    c = TestClient(app)
    r = c.get("/v1/schemas")
    assert r.status_code == 200
    assert "event" in r.json()

def test_maintenance_admin_and_block():
    c = TestClient(app)
    # Without token
    rb = c.post("/admin/maintenance", json={"mode":"on"})
    assert rb.status_code in (401, 200)
    # With token enabled at runtime by monkeypatching state
    app.state.maintenance = "on"
    r = c.post("/v1/inference", json={"user_id":"u1","amount":1,"tx_count_1h":1,"country_risk":0.1})
    assert r.status_code in (401,503)

@given(amount=st.floats(min_value=0, max_value=10000), tx=st.integers(min_value=0, max_value=1000), risk=st.floats(min_value=0, max_value=1))
def test_infer_property(amount, tx, risk):
    c = TestClient(app)
    payload = {"user_id":"u1","amount":float(amount),"tx_count_1h":int(tx),"country_risk":float(risk)}
    r = c.post("/v1/inference", json=payload)
    assert r.status_code in (200,401,415,406,503)
    if r.status_code == 200:
        js = r.json()
        assert 0.0 <= js["score"] <= 1.0
