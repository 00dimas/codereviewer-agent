"""GitHub webhook signature verification."""

from __future__ import annotations

import hashlib
import hmac
from typing import Optional


def verify_github_signature(payload: bytes, signature: Optional[str], secret: str) -> bool:
    """Return whether a request contains a valid GitHub SHA-256 signature."""
    if not signature or not signature.startswith("sha256="):
        return False

    expected = "sha256=" + hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
