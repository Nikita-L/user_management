from sqlalchemy.orm import Mapped, mapped_column

from user_management.db.base import Base


class RecentEventIdModel(Base):
    __tablename__ = "recent_event_ids"

    type: Mapped[str] = mapped_column(primary_key=True)
    recent_id: Mapped[str | None] = mapped_column()
