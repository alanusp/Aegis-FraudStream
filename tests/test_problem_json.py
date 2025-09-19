# SPDX-License-Identifier: Apache-2.0
from httpx import AsyncClient
from aegis_fraudstream.app import app

async def test_problem_json_shape():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/__nonexistent__")
        assert r.headers.get("content-type","").startswith("application/problem+json")
