from __future__ import annotations

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from config.settings import settings
from core.exceptions import PermanentProviderError, RetryableProviderError
from core.models import SMSMessage
from providers.sms.base import SMSProvider


class SNSProvider(SMSProvider):
    name = "sns"

    def __init__(self):
        self.client = boto3.client("sns", region_name=settings.aws_region)

    def send(self, message: SMSMessage) -> dict:
        attrs = {}

        if settings.sns_sender_id:
            attrs["AWS.SNS.SMS.SenderID"] = {
                "DataType": "String",
                "StringValue": settings.sns_sender_id,
            }

        try:
            result = self.client.publish(
                PhoneNumber=message.to,
                Message=message.message,
                MessageAttributes=attrs,
            )

            return {
                "provider": self.name,
                "message_id": result.get("MessageId"),
                "status": "sent",
            }

        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code in {
                "Throttled",
                "Throttling",
                "InternalError",
                "ServiceUnavailable",
            }:
                raise RetryableProviderError(str(exc)) from exc
            raise PermanentProviderError(str(exc)) from exc

        except BotoCoreError as exc:
            raise RetryableProviderError(str(exc)) from exc
