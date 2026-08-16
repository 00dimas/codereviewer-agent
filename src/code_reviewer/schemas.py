"""API response models."""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    environment: str


class WebhookResponse(BaseModel):
    status: Literal["accepted", "ignored"]
    delivery_id: str
    event: str
    reason: Optional[str] = None
