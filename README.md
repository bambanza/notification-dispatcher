# Notification Dispatcher

Reusable asynchronous email/SMS dispatcher in pure Python.

## Features

- Celery workers
- Redis broker/backend
- AWS SES email provider
- SMTP email provider
- Twilio SMS provider
- AWS SNS SMS provider
- Jinja2 templates
- Pydantic validation
- Distributed Redis rate limiting
- Retry with exponential backoff + jitter
- Retryable vs permanent provider errors
- Dead-letter storage in Redis
- Docker + Docker Compose
- Unit tests

## Architecture

Application
→ NotificationDispatcher
→ Celery/Redis
→ Worker
→ Provider adapter
→ SES / SMTP / Twilio / SNS

All Celery workers share Redis rate-limit counters, so provider quotas are
enforced globally rather than independently per worker.

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

In another shell:

```bash
python scripts/send_test.py
```

Run tests:

```bash
pytest -q
```

## Usage

```python
from core.dispatcher import dispatcher
from core.models import EmailMessage

result = dispatcher.email(
    EmailMessage(
        to=["user@example.com"],
        subject="Welcome",
        template="email/welcome.html",
        context={"name": "Emmanuel"},
    )
)

print(result.id)
```

SMS:

```python
from core.dispatcher import dispatcher
from core.models import SMSMessage

result = dispatcher.sms(
    SMSMessage(
        to="+250700000000",
        message="Your verification code is 123456",
    )
)
```

## Dead-letter handling

Permanent failures are written directly to the Redis dead-letter list.

Transient failures are retried with exponential backoff. Once retries are
exhausted, the task is dead-lettered.

Redis key:

```text
notification:dead-letter
```

You can inspect it with:

```bash
redis-cli LRANGE notification:dead-letter 0 -1
```

## Rate limiting

Provider limits are configured through environment variables:

```env
SES_RATE_LIMIT=20
SMTP_RATE_LIMIT=5
TWILIO_RATE_LIMIT=5
SNS_RATE_LIMIT=20
RATE_LIMIT_WINDOW_SECONDS=1
```

The limiter uses atomic Redis counters shared across all workers.

## Notes

For high-volume production traffic, consider replacing the fixed-window
limiter with a token-bucket implementation and storing dead letters in a
durable database or dedicated queue instead of a Redis list.


## HTTP API

The project now exposes a FastAPI service on port `8000`.

Start everything:

```bash
docker compose up --build
```

From the host:

```bash
curl http://localhost:8000/health
```

Queue an email:

```bash
curl -X POST http://localhost:8000/v1/email \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["user@example.com"],
    "subject": "Welcome",
    "template": "email/welcome.html",
    "context": {
      "name": "Emmanuel"
    }
  }'
```

Queue an SMS:

```bash
curl -X POST http://localhost:8000/v1/sms \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+250700000000",
    "message": "Your verification code is 123456"
  }'
```

Response:

```json
{
  "status": "queued",
  "channel": "email",
  "task_id": "..."
}
```

Check task status:

```bash
curl http://localhost:8000/v1/tasks/<task_id>
```

### Calling it from another Docker container

If the other container is in the same Docker Compose project/network, use the
Compose service name as the hostname:

```text
http://api:8000
```

Example Python client:

```python
import requests

response = requests.post(
    "http://api:8000/v1/email",
    json={
        "to": ["user@example.com"],
        "subject": "Welcome",
        "text_body": "Hello from another container",
    },
    timeout=10,
)

response.raise_for_status()
print(response.json())
```

Do not use `localhost:8000` from another container. Inside a container,
`localhost` refers to that container itself.
