from __future__ import annotations

from typing import Any

from pydantic import BaseModel, EmailStr, Field, field_validator


class EmailMessage(BaseModel):
    to: list[EmailStr]
    subject: str = Field(min_length=1, max_length=998)
    template: str | None = None
    text_body: str | None = None
    html_body: str | None = None
    context: dict[str, Any] = Field(default_factory=dict)
    reply_to: EmailStr | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("to")
    @classmethod
    def validate_recipients(cls, value: list[EmailStr]) -> list[EmailStr]:
        if not value:
            raise ValueError("At least one recipient is required")
        return value

    @field_validator("html_body")
    @classmethod
    def validate_body(cls, value: str | None, info):
        values = info.data
        if not value and not values.get("text_body") and not values.get("template"):
            raise ValueError("Provide template, text_body, or html_body")
        return value


class SMSMessage(BaseModel):
    to: str = Field(min_length=5, max_length=32)
    message: str = Field(min_length=1, max_length=1600)
    metadata: dict[str, Any] = Field(default_factory=dict)
