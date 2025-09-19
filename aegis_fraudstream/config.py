# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    hmac_key: str | None = None
    hmac_clock_skew_seconds: int = 300
    rate_limit_rpm: int = 120
    body_max_bytes: int = 1_048_576
    admin_token: str | None = "admin"
    model_config = SettingsConfigDict(env_prefix="AEGIS_", env_file=".env", extra="ignore")

settings = Settings()
