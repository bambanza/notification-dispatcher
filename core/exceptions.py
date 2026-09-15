class NotificationError(Exception):
    """Base exception for notification-dispatcher."""


class ValidationError(NotificationError):
    """Raised for invalid message data."""


class ProviderError(NotificationError):
    """Base exception for provider failures."""


class RetryableProviderError(ProviderError):
    """Transient provider failure that can be retried."""

    def __init__(self, message: str, retry_after: int | None = None):
        super().__init__(message)
        self.retry_after = retry_after


class PermanentProviderError(ProviderError):
    """Non-transient provider failure that should not be retried."""
