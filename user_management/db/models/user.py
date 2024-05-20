from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import String

from user_management.db.base import Base

EMAIL_MAX_LENGTH = 320


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(index=True, server_default=func.now())
    email: Mapped[str] = mapped_column(
        String(length=EMAIL_MAX_LENGTH),
        unique=True,
        nullable=False,
    )
    first_name: Mapped[str | None] = mapped_column()
    last_name: Mapped[str | None] = mapped_column()
