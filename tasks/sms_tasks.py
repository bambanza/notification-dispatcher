from __future__ import annotations

from config.celery_config import celery_app
from config.settings import settings
from core.dead_letter import save_dead_letter
from core.exceptions import PermanentProviderError, RetryableProviderError
from core.models import SMSMessage
from core.rate_limit import rate_limiter
from providers.sms.factory import get_sms_provider
from tasks.helpers import retry_delay


def _provider_limit(provider_name: str) -> int:
    return {
        "twilio": settings.twilio_rate_limit,
        "sns": settings.sns_rate_limit,
    }[provider_name]


@celery_app.task(
    bind=True,
    name="notifications.sms.send",
    max_retries=settings.max_retries,
)
def send_sms_task(self, payload: dict):
    provider = get_sms_provider()
    message = SMSMessage.model_validate(payload)

    if not rate_limiter.allow(
        key=f"provider:{provider.name}",
        limit=_provider_limit(provider.name),
        window_seconds=settings.rate_limit_window_seconds,
    ):
        raise self.retry(countdown=1)

    try:
        return provider.send(message)

    except PermanentProviderError as exc:
        save_dead_letter(
            task_name=self.name,
            payload=payload,
            error=str(exc),
            task_id=self.request.id,
            provider=provider.name,
        )
        return {
            "status": "dead-lettered",
            "provider": provider.name,
            "error": str(exc),
        }

    except RetryableProviderError as exc:
        if self.request.retries >= self.max_retries:
            save_dead_letter(
                task_name=self.name,
                payload=payload,
                error=str(exc),
                task_id=self.request.id,
                provider=provider.name,
            )
            return {
                "status": "dead-lettered",
                "provider": provider.name,
                "error": str(exc),
            }

        countdown = exc.retry_after or retry_delay(self.request.retries + 1)
        raise self.retry(exc=exc, countdown=countdown)
