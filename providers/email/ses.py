from __future__ import annotations

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from config.settings import settings
from core.exceptions import PermanentProviderError, RetryableProviderError
from core.models import EmailMessage
from core.templates import render_template
from providers.email.base import EmailProvider


class SESProvider(EmailProvider):
    name = "ses"

    def __init__(self):
        self.client = boto3.client("ses", region_name=settings.aws_region)

    def send(self, message: EmailMessage) -> dict:
        try:
            html = message.html_body
            text = message.text_body

            if message.template:
                html = render_template(message.template, message.context)

            body = {}
            if text:
                body["Text"] = {"Data": text, "Charset": "UTF-8"}
            if html:
                body["Html"] = {"Data": html, "Charset": "UTF-8"}

            response = self.client.send_email(
                Source=settings.ses_from_email,
                Destination={"ToAddresses": [str(x) for x in message.to]},
                Message={
                    "Subject": {"Data": message.subject, "Charset": "UTF-8"},
                    "Body": body,
                },
                **(
                    {"ReplyToAddresses": [str(message.reply_to)]}
                    if message.reply_to
                    else {}
                ),
            )

            return {
                "provider": self.name,
                "message_id": response.get("MessageId"),
                "status": "sent",
            }

        except ClientError as exc:
            code = exc.response.get("Error", {}).get("Code", "")
            if code in {
                "Throttling",
                "ThrottlingException",
                "ServiceUnavailable",
                "InternalFailure",
            }:
                raise RetryableProviderError(str(exc)) from exc
            raise PermanentProviderError(str(exc)) from exc

        except BotoCoreError as exc:
            raise RetryableProviderError(str(exc)) from exc
