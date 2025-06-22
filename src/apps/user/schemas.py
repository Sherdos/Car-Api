from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str
    password: str
