# SPDX-License-Identifier: Apache-2.0
from httpx import AsyncClient
from aegis_fraudstream.app import app

async def test_dsr_admin_endpoints_exist():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r1 = await ac.post("/v1/admin/dsr/block", json={"user_id":"u1"}, headers={"X-Admin-Token":"admin"})
        assert r1.status_code in (200,401,403,400)
        r2 = await ac.get("/v1/admin/dsr/status", params={"user_id":"u1"}, headers={"X-Admin-Token":"admin"})
        assert r2.status_code in (200,401,403)
        r3 = await ac.get("/v1/admin/dsr/export", params={"user_id":"u1"}, headers={"X-Admin-Token":"admin"})
        assert r3.status_code in (200,401,403)

async def test_server_timing_header():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/version")
        assert r.headers.get("Server-Timing") is not None
