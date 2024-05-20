import logging
import sys

from user_management.listener.db import Session
from user_management.listener.listeners import (
    CreateEventListener,
    DeleteEventListener,
    UpdateEventListener,
)
from user_management.listener.manager import UserEventManager, UserEventType
from user_management.services.authentication import consume_user_events

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


def process_events() -> None:
    with Session() as session:
        manager = UserEventManager(session)
        manager.subscribe(UserEventType.CREATED, CreateEventListener(session))
        manager.subscribe(UserEventType.UPDATED, UpdateEventListener(session))
        manager.subscribe(UserEventType.DELETED, DeleteEventListener(session))

        recent_id = manager.get_recent_id()
        events, recent_id = consume_user_events(recent_id)

        logger.info(f"Received {len(events)} events after event {recent_id}")
        for event in events:
            manager.notify(event.type, event.data)
        logger.info(f"Processed {len(events)} events. Recent event {recent_id}")

        if recent_id:
            manager.set_recent_id(recent_id)
