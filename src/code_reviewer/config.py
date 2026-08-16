"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional


@dataclass(frozen=True)
class Settings:
    app_env: str
    log_level: str
    github_webhook_secret: Optional[str]

    @classmethod
    def from_environment(cls) -> Settings:
        return cls(
            app_env=os.getenv("APP_ENV", "development"),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
            github_webhook_secret=os.getenv("GITHUB_WEBHOOK_SECRET"),
        )


@lru_cache
def get_settings() -> Settings:
    return Settings.from_environment()
