from __future__ import annotations

import os
from dataclasses import dataclass


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value is not None else default


@dataclass(frozen=True)
class Settings:
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")

    email_provider: str = os.getenv("EMAIL_PROVIDER", "ses").lower()
    sms_provider: str = os.getenv("SMS_PROVIDER", "twilio").lower()

    aws_region: str = os.getenv("AWS_REGION", "ca-central-1")
    ses_from_email: str = os.getenv("SES_FROM_EMAIL", "noreply@example.com")
    sns_sender_id: str | None = os.getenv("SNS_SENDER_ID")

    smtp_host: str = os.getenv("SMTP_HOST", "localhost")
    smtp_port: int = _env_int("SMTP_PORT", 587)
    smtp_username: str | None = os.getenv("SMTP_USERNAME")
    smtp_password: str | None = os.getenv("SMTP_PASSWORD")
    smtp_use_tls: bool = os.getenv("SMTP_USE_TLS", "true").lower() == "true"
    smtp_from_email: str = os.getenv("SMTP_FROM_EMAIL", "noreply@example.com")

    twilio_account_sid: str | None = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_auth_token: str | None = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_from_number: str | None = os.getenv("TWILIO_FROM_NUMBER")

    ses_rate_limit: int = _env_int("SES_RATE_LIMIT", 20)
    smtp_rate_limit: int = _env_int("SMTP_RATE_LIMIT", 5)
    twilio_rate_limit: int = _env_int("TWILIO_RATE_LIMIT", 5)
    sns_rate_limit: int = _env_int("SNS_RATE_LIMIT", 20)

    rate_limit_window_seconds: int = _env_int("RATE_LIMIT_WINDOW_SECONDS", 1)
    max_retries: int = _env_int("MAX_RETRIES", 5)
    dead_letter_key: str = os.getenv(
        "DEAD_LETTER_KEY", "notification:dead-letter"
    )


settings = Settings()
