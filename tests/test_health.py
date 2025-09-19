# SPDX-License-Identifier: Apache-2.0
from httpx import AsyncClient
from aegis_fraudstream.app import app

async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/healthz")
        assert r.status_code == 200
        assert r.json().get("ok") is True
