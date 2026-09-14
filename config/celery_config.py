from __future__ import annotations

from celery import Celery

from config.settings import settings

celery_app = Celery(
    "notification_dispatcher",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        "tasks.email_tasks",
        "tasks.sms_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
    broker_connection_retry_on_startup=True,
)
