from pydantic import BaseModel


class CarBaseSchema(BaseModel):
    name: str
    color: str
    mark_id: int


class CarCreateSchema(CarBaseSchema):
    pass


class CarReadSchema(CarBaseSchema):
    id: int

    class Config:
        from_attributes = True
