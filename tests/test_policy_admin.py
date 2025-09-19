# SPDX-License-Identifier: Apache-2.0
import json
from httpx import AsyncClient
from aegis_fraudstream.app import app

async def test_policy_admin_roundtrip():
    body = {"version":1, "thresholds": {"approve":0.2,"review":0.6,"block":0.9}}
    async with AsyncClient(app=app, base_url="http://test") as ac:
      r = await ac.post("/v1/admin/policy", content=json.dumps(body), headers={"content-type":"application/json","X-Admin-Token":"admin"})
      assert r.status_code in (200, 201, 204)
      r = await ac.post("/v1/inference", content=json.dumps({"user_id":"u","amount":1,"tx_count_1h":0,"country_risk":0.1}), headers={"content-type":"application/json"})
      assert r.status_code == 200
      j = r.json()
      assert "policy_checksum" in j
      r = await ac.delete("/v1/admin/policy", headers={"X-Admin-Token":"admin"})
      assert r.status_code in (200,204)
