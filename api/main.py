from __future__ import annotations

from fastapi import FastAPI, HTTPException, status

from core.dispatcher import dispatcher
from core.models import EmailMessage, SMSMessage
from core.redis_client import redis_client

app = FastAPI(
    title="Notification Dispatcher API",
    version="1.0.0",
    description="HTTP API for queueing asynchronous email and SMS notifications.",
)


@app.get("/health")
def health():
    try:
        redis_client.ping()
        redis_status = "ok"
    except Exception:
        redis_status = "unavailable"

    return {
        "status": "ok" if redis_status == "ok" else "degraded",
        "redis": redis_status,
    }


@app.post("/v1/email", status_code=status.HTTP_202_ACCEPTED)
def queue_email(message: EmailMessage):
    try:
        result = dispatcher.email(message)
        return {
            "status": "queued",
            "channel": "email",
            "task_id": result.id,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Unable to queue email: {exc}",
        ) from exc


@app.post("/v1/sms", status_code=status.HTTP_202_ACCEPTED)
def queue_sms(message: SMSMessage):
    try:
        result = dispatcher.sms(message)
        return {
            "status": "queued",
            "channel": "sms",
            "task_id": result.id,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Unable to queue SMS: {exc}",
        ) from exc


@app.get("/v1/tasks/{task_id}")
def task_status(task_id: str):
    result = dispatcher.result(task_id)

    response = {
        "task_id": task_id,
        "state": result.state,
    }

    if result.successful():
        response["result"] = result.result
    elif result.failed():
        response["error"] = str(result.result)

    return response
