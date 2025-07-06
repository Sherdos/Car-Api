from pydantic import BaseModel

from src.apps.user.schemas import UserBaseSchema


class CarBaseSchema(BaseModel):
    name: str
    color: str
    mark_id: int
    image_url: str


class CarCreateSchema(CarBaseSchema):
    pass


class CarReadSchema(CarBaseSchema):
    id: int
    user_id: int

    class Config:
        from_attributes = True
