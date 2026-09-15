from __future__ import annotations

import smtplib
from email.message import EmailMessage as MIMEEmailMessage

from config.settings import settings
from core.exceptions import PermanentProviderError, RetryableProviderError
from core.models import EmailMessage
from core.templates import render_template
from providers.email.base import EmailProvider


class SMTPProvider(EmailProvider):
    name = "smtp"

    def send(self, message: EmailMessage) -> dict:
        mime = MIMEEmailMessage()
        mime["From"] = settings.smtp_from_email
        mime["To"] = ", ".join(str(x) for x in message.to)
        mime["Subject"] = message.subject

        if message.reply_to:
            mime["Reply-To"] = str(message.reply_to)

        text_body = message.text_body or ""
        html_body = message.html_body

        if message.template:
            html_body = render_template(message.template, message.context)

        mime.set_content(text_body or " ")
        if html_body:
            mime.add_alternative(html_body, subtype="html")

        try:
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as smtp:
                if settings.smtp_use_tls:
                    smtp.starttls()

                if settings.smtp_username:
                    smtp.login(settings.smtp_username, settings.smtp_password or "")

                smtp.send_message(mime)

            return {"provider": self.name, "status": "sent"}

        except smtplib.SMTPRecipientsRefused as exc:
            raise PermanentProviderError(str(exc)) from exc
        except smtplib.SMTPException as exc:
            raise RetryableProviderError(str(exc)) from exc
        except OSError as exc:
            raise RetryableProviderError(str(exc)) from exc
