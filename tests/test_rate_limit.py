from unittest.mock import patch

from core.rate_limit import RedisRateLimiter


def test_rate_limit_allows_within_limit():
    limiter = RedisRateLimiter()

    with patch("core.rate_limit.redis_client.eval", return_value=2):
        assert limiter.allow("provider:test", limit=5) is True


def test_rate_limit_blocks_above_limit():
    limiter = RedisRateLimiter()

    with patch("core.rate_limit.redis_client.eval", return_value=6):
        assert limiter.allow("provider:test", limit=5) is False
