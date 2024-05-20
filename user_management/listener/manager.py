from abc import ABC, abstractmethod
from collections import defaultdict
from enum import StrEnum, auto
from typing import Any

from pydantic import BaseModel
from sqlalchemy.orm import Session

from user_management.db.models.event import RecentEventIdModel


class UserEventType(StrEnum):
    CREATED = auto()
    UPDATED = auto()
    DELETED = auto()


class Event(BaseModel):
    type: UserEventType
    data: dict[str, Any]


class EventListener(ABC):
    def __init__(self, session: Session) -> None:
        self.session = session

    @abstractmethod
    def update(self, data: dict[str, Any]) -> None:
        raise NotImplementedError()


class UserEventManager:
    DB_EVENT_TYPE = "user_events"

    listeners: dict[UserEventType, list[EventListener]] = defaultdict(list)

    def __init__(self, session: Session) -> None:
        self.session = session

    @classmethod
    def subscribe(cls, event: UserEventType, listener: EventListener) -> None:
        cls.listeners[event].append(listener)

    def notify(self, event: UserEventType, data: dict[str, Any]) -> None:
        for listener in self.listeners[event]:
            listener.update(data)
        self.session.commit()

    def get_recent_id(self) -> str | None:
        event = self.session.get(RecentEventIdModel, self.DB_EVENT_TYPE)
        if event:
            return event.recent_id
        return None

    def set_recent_id(self, recent_id: str) -> None:
        event = RecentEventIdModel(recent_id=recent_id, type=self.DB_EVENT_TYPE)
        self.session.merge(event)
        self.session.commit()
