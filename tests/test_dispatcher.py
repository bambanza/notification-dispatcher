from unittest.mock import patch

from core.dispatcher import NotificationDispatcher
from core.models import EmailMessage, SMSMessage


def test_dispatcher_email():
    dispatcher = NotificationDispatcher()

    with patch("core.dispatcher.celery_app.send_task") as send_task:
        dispatcher.email(
            EmailMessage(
                to=["user@example.com"],
                subject="Test",
                text_body="Hello",
            )
        )

        send_task.assert_called_once()


def test_dispatcher_sms():
    dispatcher = NotificationDispatcher()

    with patch("core.dispatcher.celery_app.send_task") as send_task:
        dispatcher.sms(
            SMSMessage(
                to="+250700000000",
                message="Hello",
            )
        )

        send_task.assert_called_once()
