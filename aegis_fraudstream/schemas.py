# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Dict, Any

class Event(BaseModel):
    user_id: str = Field(min_length=1, max_length=128)
    amount: float = Field(ge=0)
    tx_count_1h: int = Field(ge=0, le=10000)
    country_risk: float = Field(ge=0, le=1)

class ScoreResponse(BaseModel):
    score: float = Field(ge=0, le=1)
    features: Dict[str, Any] | None = None
    decision: str | None = None
    reason: str | None = None
