# SPDX-License-Identifier: Apache-2.0
import json, time
from fastapi.testclient import TestClient
from aegis_fraudstream.app import app
from aegis_fraudstream.config import settings

def test_idempotency_with_redis(monkeypatch):
    try:
        import fakeredis  # type: ignore
    except Exception:
        return  # skip if not available
    fake = fakeredis.FakeRedis()
    monkeypatch.setenv("AEGIS_REDIS_URL", "redis://localhost:6379/0")
    from aegis_fraudstream import config as cfg
    cfg.settings.redis_url = "redis://localhost:6379/0"  # type: ignore[attr-defined]
    import redis  # type: ignore
    monkeypatch.setattr(redis, "from_url", lambda *_a, **_k: fake)
    c = TestClient(app)
    payload = {"user_id":"u1","amount":1,"tx_count_1h":1,"country_risk":0.1}
    headers = {"Idempotency-Key": "abc123"}
    r1 = c.post("/v1/inference", json=payload, headers=headers)
    r2 = c.post("/v1/inference", json=payload, headers=headers)
    assert r1.status_code == r2.status_code
    assert r2.text == r1.text
