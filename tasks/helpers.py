from __future__ import annotations

import random


def retry_delay(retries: int, base: int = 2, max_seconds: int = 300) -> int:
    # Exponential backoff + a little jitter to avoid retry storms.
    delay = min(base ** max(retries, 1), max_seconds)
    return delay + random.randint(0, min(3, delay))
