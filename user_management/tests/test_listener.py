from unittest.mock import MagicMock

import pytest

from user_management.listener.listeners import (
    CreateEventListener,
    DeleteEventListener,
    UpdateEventListener,
)
from user_management.listener.manager import Event, UserEventManager, UserEventType

USER_DATA = {
    "id": "user_id",
    "email": "test@test.com",
    "last_name": "test@test.com",
    "first_name": "test@test.com",
    "created_at": "2021-06-25T19:07:33.155Z",
}

CREATE_EVENT = Event(type=UserEventType.CREATED, data=USER_DATA)
UPDATE_EVENT = Event(type=UserEventType.UPDATED, data=USER_DATA)
DELETE_EVENT = Event(type=UserEventType.DELETED, data=USER_DATA)


@pytest.mark.parametrize("event", [CREATE_EVENT, UPDATE_EVENT])
def test_create_or_update(event):
    session = MagicMock()

    manager = UserEventManager(session)
    manager.subscribe(UserEventType.CREATED, CreateEventListener(session))
    manager.subscribe(UserEventType.UPDATED, UpdateEventListener(session))

    manager.notify(event.type, event.data)

    created_user = session.merge.call_args.args[0]
    created_user.id = USER_DATA["id"]
    created_user.email = USER_DATA["email"]
    created_user.last_name = USER_DATA["last_name"]
    created_user.first_name = USER_DATA["first_name"]
    created_user.created_at = USER_DATA["created_at"]
    session.merge.assert_called_once()
    session.commit.assert_called_once()


def test_delete():
    session = MagicMock()

    manager = UserEventManager(session)
    manager.subscribe(UserEventType.DELETED, DeleteEventListener(session))

    manager.notify(DELETE_EVENT.type, DELETE_EVENT.data)

    statement = session.execute.call_args.args[0]
    query = str(statement.compile(compile_kwargs={"literal_binds": True}))
    assert query == "DELETE FROM users WHERE users.id = 'user_id'"
    session.execute.assert_called_once()
    session.commit.assert_called_once()
