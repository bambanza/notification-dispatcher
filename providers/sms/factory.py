from __future__ import annotations

from config.settings import settings
from providers.sms.base import SMSProvider
from providers.sms.sns import SNSProvider
from providers.sms.twilio import TwilioProvider


def get_sms_provider(name: str | None = None) -> SMSProvider:
    provider = (name or settings.sms_provider).lower()

    if provider == "twilio":
        return TwilioProvider()
    if provider == "sns":
        return SNSProvider()

    raise ValueError(f"Unsupported SMS provider: {provider}")
