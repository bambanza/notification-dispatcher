from __future__ import annotations

import time

from core.redis_client import redis_client


class RedisRateLimiter:
    """
    Fixed-window distributed rate limiter backed by Redis.

    All workers share the same counters, so the limit is global across workers.
    """

    LUA_SCRIPT = """
    local current = redis.call("INCR", KEYS[1])
    if current == 1 then
        redis.call("EXPIRE", KEYS[1], ARGV[1])
    end
    return current
    """

    def allow(self, key: str, limit: int, window_seconds: int = 1) -> bool:
        bucket = int(time.time() // window_seconds)
        redis_key = f"ratelimit:{key}:{bucket}"

        current = redis_client.eval(
            self.LUA_SCRIPT,
            1,
            redis_key,
            window_seconds + 1,
        )

        return int(current) <= limit


rate_limiter = RedisRateLimiter()
