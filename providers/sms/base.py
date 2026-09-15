from __future__ import annotations

from abc import ABC, abstractmethod

from core.models import SMSMessage


class SMSProvider(ABC):
    name: str

    @abstractmethod
    def send(self, message: SMSMessage) -> dict:
        raise NotImplementedError
