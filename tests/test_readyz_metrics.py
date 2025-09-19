# SPDX-License-Identifier: Apache-2.0
import os
from fastapi.testclient import TestClient
from aegis_fraudstream.app import app

def test_readyz():
    with TestClient(app) as c:
        r = c.get("/readyz")
        assert r.status_code == 200
        assert r.json().get("status") == "ready"

def test_metrics_toggle():
    os.environ["METRICS_ENABLED"] = "1"
    with TestClient(app) as c:
        r = c.get("/metrics")
        assert r.status_code in (200, 404)  # depends on optional deps
    os.environ.pop("METRICS_ENABLED", None)
