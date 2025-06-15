from pydantic import BaseModel


class CarBaseSchema(BaseModel):
    name: str
    color: str
    mark: str


class CarCreateSchema(CarBaseSchema):
    pass


class CarReadSchema(CarBaseSchema):
    id: int
