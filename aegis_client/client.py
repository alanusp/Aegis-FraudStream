# SPDX-License-Identifier: Apache-2.0
import os, json, hmac, hashlib, base64, typing as t
import httpx

class Client:
    def __init__(self, base_url: str, api_key: str | None = None, timeout: float = 5.0):
        self.base = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
    def _headers(self):
        h = {"content-type":"application/json"}
        if self.api_key: h["X-API-Key"] = self.api_key
        return h
    def inference(self, user_id: str, amount: float, tx_count_1h: int, country_risk: float) -> dict:
        body = {"user_id": user_id, "amount": amount, "tx_count_1h": tx_count_1h, "country_risk": country_risk}
        with httpx.Client(timeout=self.timeout) as c:
            r = c.post(f"{self.base}/v1/inference", json=body, headers=self._headers())
            r.raise_for_status(); return r.json()
    def batch_inference(self, items: list[dict]) -> list[dict]:
        with httpx.Client(timeout=self.timeout) as c:
            r = c.post(f"{self.base}/v1/batch/inference", json=items, headers=self._headers())
            r.raise_for_status(); return r.json()
    @staticmethod
    def verify_signature(obj: t.Any, signature_b64: str, key: str) -> bool:
        payload = json.dumps(obj, sort_keys=True, separators=(',',':')).encode()
        calc = base64.b64encode(hmac.new(key.encode(), payload, hashlib.sha256).digest()).decode()
        return hmac.compare_digest(calc, signature_b64)
