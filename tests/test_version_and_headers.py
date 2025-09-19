# SPDX-License-Identifier: Apache-2.0
from httpx import AsyncClient
from aegis_fraudstream.app import app

async def test_version_and_headers():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/version")
        assert r.status_code == 200
        r = await ac.post("/v1/inference", json={"user_id":"u1","amount":1,"tx_count_1h":0,"country_risk":0.1})
        assert r.status_code == 200
        assert r.headers.get("X-Frame-Options") == "DENY"
        assert "default-src 'self'" in r.headers.get("Content-Security-Policy","")
