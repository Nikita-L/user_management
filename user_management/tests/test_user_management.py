from http import HTTPStatus

import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from user_management.db.dao.user_dao import UserDAO
from user_management.services.authentication import CreateUserError
from user_management.web.api.users.schema import UserCreateRequest


@pytest.mark.anyio
async def test_get_users(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
):
    per_page = 10
    users_num = 11
    skip = 2
    expected_users_count = min(users_num - skip, per_page)

    dao = UserDAO(dbsession)
    for i in range(users_num):
        await dao.create_user(
            id_=str(i),
            email=f"{i}@test.com",
            first_name=f"First {i}",
            last_name=f"Last {i}",
        )

    url = fastapi_app.url_path_for("get_users")
    response = await client.get(url, params={"skip": skip, "limit": per_page})
    users = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert users["total"] == users_num
    assert users["skip"] == skip
    assert users["count"] == len(users["items"]) == expected_users_count

    for i in range(expected_users_count):
        user_id = i + skip
        assert users["items"][i]["id"] == str(user_id)
        assert users["items"][i]["email"] == f"{user_id}@test.com"
        assert users["items"][i]["first_name"] == f"First {user_id}"
        assert users["items"][i]["last_name"] == f"Last {user_id}"


@pytest.mark.anyio
async def test_create(
    mocker,
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
):
    new_user_id = "user_id"
    mocker.patch(
        "user_management.services.authentication.create_user",
        return_value=new_user_id,
    )
    new_user = UserCreateRequest(
        email="test@test.com",
        password="hardpassword123#",
        first_name="Test First",
        last_name="Test Last",
    )

    url = fastapi_app.url_path_for("create_user")
    response = await client.post(url, json=new_user.dict())

    assert response.status_code == HTTPStatus.CREATED

    user_dao = UserDAO(dbsession)
    users, total_users = await user_dao.get_all_users(skip=0, limit=1)
    created_user = users[0]

    assert total_users == 1
    assert created_user.id == new_user_id
    assert created_user.email == new_user.email
    assert created_user.first_name == new_user.first_name
    assert created_user.last_name == new_user.last_name


@pytest.mark.anyio
async def test_create_easy_password(
    mocker,
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
):
    error_msg = "Password does not meet strength requirements."
    mocker.patch(
        "user_management.services.authentication.create_user",
        return_value=CreateUserError(error_msg),
    )
    user = UserCreateRequest(
        email="test@test.com",
        password="123456789",
        first_name="Test First",
        last_name="Test Last",
    )

    url = fastapi_app.url_path_for("create_user")
    response = await client.post(url, json=user.dict())

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == error_msg


@pytest.mark.anyio
async def test_create_already_existing(
    mocker,
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
):
    error_msg = "Could not create user."
    mocker.patch(
        "user_management.services.authentication.create_user",
        return_value=CreateUserError(error_msg),
    )
    user = UserCreateRequest(
        email="test@test.com",
        password="hardpassword123#",
        first_name="Test First",
        last_name="Test Last",
    )

    url = fastapi_app.url_path_for("create_user")
    response = await client.post(url, json=user.dict())

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == error_msg
