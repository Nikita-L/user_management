from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from user_management.db.dao.user_dao import UserDAO
from user_management.services import authentication
from user_management.web.api.users.schema import (
    UserCreateRequest,
    UserResponse,
    UsersResponse,
)

router = APIRouter()


@router.get("/")
async def get_users(
    skip: int = 0,
    limit: int = 10,
    user_dao: UserDAO = Depends(),
) -> UsersResponse:
    user_models, total_rows = await user_dao.get_all_users(skip, limit)
    users = [UserResponse.model_validate(model) for model in user_models]
    return UsersResponse(
        skip=skip,
        limit=limit,
        items=users,
        total=total_rows,
        count=len(users),
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreateRequest,
    background_tasks: BackgroundTasks,
    user_dao: UserDAO = Depends(),
) -> None:
    id_ = authentication.create_user(
        user.email,
        user.password.get_secret_value(),
        user.first_name,
        user.last_name,
    )
    if isinstance(id_, authentication.CreateUserError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=id_.message)

    background_tasks.add_task(
        user_dao.create_user,
        id_,
        user.email,
        user.first_name,
        user.last_name,
    )
