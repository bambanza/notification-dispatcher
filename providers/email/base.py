from __future__ import annotations

from abc import ABC, abstractmethod

from core.models import EmailMessage


class EmailProvider(ABC):
    name: str

    @abstractmethod
    def send(self, message: EmailMessage) -> dict:
        raise NotImplementedError
