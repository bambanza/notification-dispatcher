from __future__ import annotations

from celery.result import AsyncResult

from config.celery_config import celery_app
from core.models import EmailMessage, SMSMessage


class NotificationDispatcher:
    def email(self, message: EmailMessage):
        return celery_app.send_task(
            "notifications.email.send",
            args=[message.model_dump(mode="json")],
        )

    def sms(self, message: SMSMessage):
        return celery_app.send_task(
            "notifications.sms.send",
            args=[message.model_dump(mode="json")],
        )

    def result(self, task_id: str) -> AsyncResult:
        return AsyncResult(task_id, app=celery_app)


dispatcher = NotificationDispatcher()
