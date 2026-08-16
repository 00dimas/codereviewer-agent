"""API behavior tests."""

import hashlib
import hmac
import json
from typing import Any

from fastapi.testclient import TestClient


def signed_headers(
    payload: bytes,
    secret: str,
    *,
    event: str = "pull_request",
    delivery_id: str = "delivery-123",
) -> dict[str, str]:
    digest = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return {
        "X-GitHub-Event": event,
        "X-GitHub-Delivery": delivery_id,
        "X-Hub-Signature-256": f"sha256={digest}",
        "Content-Type": "application/json",
    }


def encode(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, separators=(",", ":")).encode()


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "environment": "test"}


def test_accepts_supported_pull_request_event(client: TestClient, webhook_secret: str) -> None:
    payload = encode({"action": "opened", "pull_request": {"number": 42}})

    response = client.post(
        "/webhooks/github",
        content=payload,
        headers=signed_headers(payload, webhook_secret),
    )

    assert response.status_code == 202
    assert response.json() == {
        "status": "accepted",
        "delivery_id": "delivery-123",
        "event": "pull_request",
        "reason": None,
    }


def test_ignores_unsupported_event(client: TestClient, webhook_secret: str) -> None:
    payload = encode({"zen": "Keep it logically awesome."})

    response = client.post(
        "/webhooks/github",
        content=payload,
        headers=signed_headers(payload, webhook_secret, event="ping"),
    )

    assert response.status_code == 202
    assert response.json()["status"] == "ignored"
    assert response.json()["reason"] == "event is not a pull_request"


def test_rejects_invalid_signature(client: TestClient) -> None:
    payload = encode({"action": "opened"})
    headers = {
        "X-GitHub-Event": "pull_request",
        "X-GitHub-Delivery": "delivery-123",
        "X-Hub-Signature-256": "sha256=invalid",
    }

    response = client.post("/webhooks/github", content=payload, headers=headers)

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid GitHub webhook signature"}


def test_rejects_missing_github_headers(client: TestClient) -> None:
    response = client.post("/webhooks/github", json={"action": "opened"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Missing required GitHub event headers"}
