"""Webhook event routing for the M0 backbone."""

from __future__ import annotations

from typing import Any, Optional

SUPPORTED_PULL_REQUEST_ACTIONS = {"opened", "reopened", "synchronize"}


def classify_event(event: str, payload: dict[str, Any]) -> tuple[str, Optional[str]]:
    """Classify a webhook without starting review work yet."""
    if event != "pull_request":
        return "ignored", "event is not a pull_request"

    action = payload.get("action")
    if action not in SUPPORTED_PULL_REQUEST_ACTIONS:
        return "ignored", f"pull_request action '{action}' is not supported"

    return "accepted", None
