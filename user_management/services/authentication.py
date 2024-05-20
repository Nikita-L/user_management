import workos
from workos.exceptions import BadRequestException

from user_management.listener.manager import Event, UserEventType
from user_management.settings import settings

workos.api_key = settings.workos_api_key
workos.client_id = settings.workos_client_id


EVENT_TYPE_BY_ID = {
    "user.created": UserEventType.CREATED,
    "user.updated": UserEventType.UPDATED,
    "user.deleted": UserEventType.DELETED,
}


class CreateUserError:
    def __init__(self, message: str):
        self.message = message


def create_user(
    email: str,
    password: str,
    first_name: str | None,
    last_name: str | None,
) -> str | CreateUserError:

    try:
        resp = workos.client.user_management.create_user(
            {
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
            },
        )
    except BadRequestException as exception:
        return CreateUserError(exception.message)

    return resp["id"]


def consume_user_events(after: str | None = None) -> tuple[list[Event], str | None]:
    resp = workos.client.events.list_events(
        events=list(EVENT_TYPE_BY_ID.keys()),
        after=after,
    )

    events = []
    for event_raw in resp["data"]:
        event = Event(type=EVENT_TYPE_BY_ID[event_raw["event"]], data=event_raw["data"])
        events.append(event)

    if not events:
        return events, after

    recent_after = resp["data"][-1]["id"]
    return events, recent_after
