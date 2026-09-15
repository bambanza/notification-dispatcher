from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from config.settings import settings
from core.redis_client import redis_client


def save_dead_letter(
    *,
    task_name: str,
    payload: dict[str, Any],
    error: str,
    task_id: str | None = None,
    provider: str | None = None,
) -> None:
    record = {
        "task_id": task_id,
        "task_name": task_name,
        "provider": provider,
        "payload": payload,
        "error": error,
        "failed_at": datetime.now(timezone.utc).isoformat(),
    }

    redis_client.rpush(settings.dead_letter_key, json.dumps(record))


def list_dead_letters(limit: int = 100) -> list[dict[str, Any]]:
    rows = redis_client.lrange(settings.dead_letter_key, 0, max(limit - 1, 0))
    return [json.loads(row) for row in rows]
