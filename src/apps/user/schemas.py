from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    password: str


class UserCreateSchema(UserBaseSchema):
    username: str
    email: str


class UserUpdateSchema(UserBaseSchema):
    email: str | None
    username: str | None
