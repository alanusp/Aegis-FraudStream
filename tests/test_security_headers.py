# SPDX-License-Identifier: Apache-2.0
from fastapi.testclient import TestClient
from aegis_fraudstream.app import app

def test_security_headers_present():
    c = TestClient(app)
    r = c.get("/health")
    for k in ["X-Content-Type-Options","X-Frame-Options","Strict-Transport-Security","Referrer-Policy"]:
        assert k in r.headers
