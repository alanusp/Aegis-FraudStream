# SPDX-License-Identifier: Apache-2.0
from httpx import AsyncClient
from aegis_fraudstream.app import app

async def test_admin_logs_endpoint_exists():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/v1/admin/logs", headers={"X-Admin-Token":"admin"})
        assert r.status_code in (200,401,403)
