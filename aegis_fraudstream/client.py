# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any
import httpx
from .schemas import Event, ScoreResponse

DEFAULT_TIMEOUT = 5.0

@dataclass
class ClientConfig:
    base_url: str = "http://localhost:8080"
    api_key: Optional[str] = None
    timeout: float = DEFAULT_TIMEOUT

class AegisClient:
    def __init__(self, config: ClientConfig | None = None):
        self.config = config or ClientConfig()
        headers = {}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        self._client = httpx.Client(base_url=self.config.base_url, timeout=self.config.timeout, headers=headers)

    def close(self) -> None:
        self._client.close()

    def score(self, event: Event) -> ScoreResponse:
        r = self._client.post("/v1/score", json=event.model_dump())
        r.raise_for_status()
        return ScoreResponse.model_validate(r.json())

class AegisAsyncClient:
    def __init__(self, config: ClientConfig | None = None):
        self.config = config or ClientConfig()
        headers = {}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        self._client = httpx.AsyncClient(base_url=self.config.base_url, timeout=self.config.timeout, headers=headers)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def score(self, event: Event) -> ScoreResponse:
        r = await self._client.post("/v1/score", json=event.model_dump())
        r.raise_for_status()
        return ScoreResponse.model_validate(r.json())
