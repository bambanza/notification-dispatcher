import os

# Network configuration
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:6379/0"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:6379/0"

# Production task settings
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TIMEZONE = "UTC"
CELERY_ENABLE_UTC = True

# Throttling third-party APIs to prevent rate limits
CELERY_ANNOTATIONS = {
    "tasks.email_tasks.send_transactional_email": {"rate_limit": "50/m"},
    "tasks.sms_tasks.send_sms_notification": {"rate_limit": "20/m"},
}
