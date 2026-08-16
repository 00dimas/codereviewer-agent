"""FastAPI entrypoint for CodeReviewer Agent."""

from __future__ import annotations

import json
import logging
from typing import Annotated, Any, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status

from .config import Settings, get_settings
from .schemas import HealthResponse, WebhookResponse
from .security import verify_github_signature
from .webhooks import classify_event

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    logging.basicConfig(level=getattr(logging, settings.log_level, logging.INFO))

    app = FastAPI(
        title="CodeReviewer Agent",
        description="Webhook backbone for automated GitHub pull request reviews.",
        version="0.1.0",
    )

    @app.get("/health", response_model=HealthResponse, tags=["system"])
    async def health(settings: Annotated[Settings, Depends(get_settings)]) -> HealthResponse:
        return HealthResponse(environment=settings.app_env)

    @app.post(
        "/webhooks/github",
        response_model=WebhookResponse,
        status_code=status.HTTP_202_ACCEPTED,
        tags=["webhooks"],
    )
    async def github_webhook(
        request: Request,
        settings: Annotated[Settings, Depends(get_settings)],
        x_github_event: Annotated[Optional[str], Header()] = None,
        x_github_delivery: Annotated[Optional[str], Header()] = None,
        x_hub_signature_256: Annotated[Optional[str], Header()] = None,
    ) -> WebhookResponse:
        if not settings.github_webhook_secret:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="GitHub webhook secret is not configured",
            )
        if not x_github_event or not x_github_delivery:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required GitHub event headers",
            )

        body = await request.body()
        if not verify_github_signature(body, x_hub_signature_256, settings.github_webhook_secret):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid GitHub webhook signature",
            )

        try:
            payload: dict[str, Any] = json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Webhook payload must be valid JSON",
            ) from error

        event_status, reason = classify_event(x_github_event, payload)
        logger.info(
            "GitHub webhook received",
            extra={
                "delivery_id": x_github_delivery,
                "github_event": x_github_event,
                "event_status": event_status,
            },
        )
        return WebhookResponse(
            status=event_status,
            delivery_id=x_github_delivery,
            event=x_github_event,
            reason=reason,
        )

    return app


app = create_app()
