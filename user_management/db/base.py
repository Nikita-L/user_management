from sqlalchemy.orm import DeclarativeBase

from user_management.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
