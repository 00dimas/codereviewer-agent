"""Shared test fixtures."""

import pytest
from fastapi.testclient import TestClient

from code_reviewer.config import Settings, get_settings
from code_reviewer.main import app


@pytest.fixture
def webhook_secret() -> str:
    return "test-webhook-secret"


@pytest.fixture
def client(webhook_secret: str) -> TestClient:
    app.dependency_overrides[get_settings] = lambda: Settings(
        app_env="test",
        log_level="DEBUG",
        github_webhook_secret=webhook_secret,
    )
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
