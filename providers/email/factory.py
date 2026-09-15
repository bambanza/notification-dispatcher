from __future__ import annotations

from config.settings import settings
from providers.email.base import EmailProvider
from providers.email.ses import SESProvider
from providers.email.smtp import SMTPProvider


def get_email_provider(name: str | None = None) -> EmailProvider:
    provider = (name or settings.email_provider).lower()

    if provider == "ses":
        return SESProvider()
    if provider == "smtp":
        return SMTPProvider()

    raise ValueError(f"Unsupported email provider: {provider}")
