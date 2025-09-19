# SPDX-License-Identifier: Apache-2.0
import anyio
import json
from httpx import AsyncClient
from aegis_fraudstream.app import app

async def _post(client, path, payload):
    return await client.post(path, content=json.dumps(payload), headers={"content-type":"application/json"})

async def test_ready_and_infer():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/ready"); assert r.status_code in (200, 204)
        r = await _post(ac, "/v1/inference", {"user_id":"u1","amount":10,"tx_count_1h":1,"country_risk":0.1})
        assert r.status_code == 200
        body = r.json()
        assert "score" in body and "decision" in body
