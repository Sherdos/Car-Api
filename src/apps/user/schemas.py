from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    id: int
    username: str
    email: str


class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str


class UserUpdateSchema(BaseModel):
    email: str | None
    username: str | None
    password: str | None
