from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr, field_serializer


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    first_name: str | None
    last_name: str | None


class UsersResponse(BaseModel):
    total: int
    limit: int
    skip: int
    count: int
    items: list[UserResponse]


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: SecretStr
    first_name: str
    last_name: str

    @field_serializer("password", when_used="always")
    def dump_secret(self, value: SecretStr) -> str:
        return value.get_secret_value()
