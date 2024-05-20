from fastapi import Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from user_management.db.dependencies import get_db_session
from user_management.db.models.user import UserModel


class UserDAO:
    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_user(
        self,
        id_: str,
        email: str,
        first_name: str | None,
        last_name: str | None,
    ) -> None:
        user = UserModel(
            id=id_,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        self.session.add(user)
        await self.session.commit()

    async def get_all_users(
        self,
        skip: int,
        limit: int,
    ) -> tuple[list[UserModel], int]:
        query = select(func.count(UserModel.id))
        result = await self.session.execute(query)
        total_rows = result.one()

        query = select(UserModel).order_by(  # type: ignore [assignment]
            UserModel.created_at,
        )
        query = query.limit(limit).offset(skip)
        result = await self.session.scalars(query)  # type: ignore [assignment]
        users = result.all()

        return list(users), int(total_rows[0])  # type: ignore [arg-type]
