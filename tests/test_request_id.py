# SPDX-License-Identifier: Apache-2.0
from fastapi.testclient import TestClient
from aegis_fraudstream.app import app

def test_request_id_header_present():
    c = TestClient(app)
    r = c.get("/health")
    assert r.headers.get("X-Request-ID") is not None
