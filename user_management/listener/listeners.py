import logging
from typing import Any

from sqlalchemy import delete

from user_management.db.models.user import UserModel
from user_management.listener.manager import EventListener

logger = logging.getLogger(__name__)


def user_from_data(data: dict[str, Any]) -> UserModel:
    return UserModel(
        id=data["id"],
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        created_at=data["created_at"],
    )


class CreateEventListener(EventListener):
    def update(self, data: dict[str, Any]) -> None:
        user = user_from_data(data)
        self.session.merge(user)


class UpdateEventListener(EventListener):
    def update(self, data: dict[str, Any]) -> None:
        user = user_from_data(data)
        self.session.merge(user)


class DeleteEventListener(EventListener):
    def update(self, data: dict[str, Any]) -> None:
        query = delete(UserModel).where(UserModel.id == data["id"])
        self.session.execute(query)
