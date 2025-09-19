# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations
import time
import threading
from typing import Callable, Dict, Tuple
from starlette.types import ASGIApp, Receive, Scope, Send

class TokenBucket:
    def __init__(self, rate: float, capacity: int):
        self.rate = float(rate)
        self.capacity = int(capacity)
        self.tokens = float(capacity)
        self.timestamp = time.monotonic()
        self.lock = threading.Lock()

    def allow(self) -> bool:
        now = time.monotonic()
        with self.lock:
            elapsed = now - self.timestamp
            self.timestamp = now
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                return True
            return False

class RateLimitMiddleware:
    def __init__(self, app: ASGIApp, rate: float = 50.0, capacity: int = 100):
        self.app = app
        self.rate = rate
        self.capacity = capacity
        self.buckets: Dict[str, TokenBucket] = {}
        self.lock = threading.Lock()

    def _key(self, scope: Scope) -> str:
        client = scope.get("client") or ("", 0)
        return f"{client[0]}"

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        key = self._key(scope)
        with self.lock:
            bucket = self.buckets.get(key)
            if bucket is None:
                bucket = self.buckets.setdefault(key, TokenBucket(self.rate, self.capacity))
        if not bucket.allow():
            await send({
                "type": "http.response.start",
                "status": 429,
                "headers": [(b"content-type", b"application/json")],
            })
            await send({"type": "http.response.body", "body": b'{"error":"rate_limited"}'})
            return
        await self.app(scope, receive, send)
