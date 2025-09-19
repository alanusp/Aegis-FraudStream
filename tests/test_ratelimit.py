# SPDX-License-Identifier: Apache-2.0
import os
from fastapi.testclient import TestClient
from aegis_fraudstream.app import app

def test_rate_limit_toggle():
    os.environ["RATE_LIMIT_ENABLED"] = "1"
    with TestClient(app) as c:
        # exhaust a few tokens quickly
        for _ in range(200):
            r = c.get("/health")
        # eventually expect 429
        got_429 = any(c.get("/health").status_code == 429 for _ in range(50))
        assert got_429
    os.environ.pop("RATE_LIMIT_ENABLED", None)
