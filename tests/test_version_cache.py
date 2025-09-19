# SPDX-License-Identifier: Apache-2.0
from aegis_fraudstream.app import app
from httpx import AsyncClient

async def test_version_etag_conditional():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r1 = await ac.get("/version")
        assert r1.status_code == 200
        et = r1.headers.get("ETag")
        r2 = await ac.get("/version", headers={"If-None-Match": et})
        assert r2.status_code == 304
