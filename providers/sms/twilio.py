from __future__ import annotations

from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from config.settings import settings
from core.exceptions import PermanentProviderError, RetryableProviderError
from core.models import SMSMessage
from providers.sms.base import SMSProvider


class TwilioProvider(SMSProvider):
    name = "twilio"

    def __init__(self):
        if not settings.twilio_account_sid or not settings.twilio_auth_token:
            raise PermanentProviderError("Twilio credentials are not configured")

        if not settings.twilio_from_number:
            raise PermanentProviderError("TWILIO_FROM_NUMBER is not configured")

        self.client = Client(
            settings.twilio_account_sid,
            settings.twilio_auth_token,
        )

    def send(self, message: SMSMessage) -> dict:
        try:
            result = self.client.messages.create(
                to=message.to,
                from_=settings.twilio_from_number,
                body=message.message,
            )

            return {
                "provider": self.name,
                "message_id": result.sid,
                "status": result.status,
            }

        except TwilioRestException as exc:
            if exc.status in {429, 500, 502, 503, 504}:
                raise RetryableProviderError(str(exc)) from exc
            raise PermanentProviderError(str(exc)) from exc
