from sqlmodel import Session
from src.apps.car.models import Car
from src.apps.car.schemas import CarCreateSchema


class CarRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, car_id: int) -> Car | None:
        return self.session.query(Car).filter(Car.id == car_id).first()

    def create(self, car_data: CarCreateSchema) -> Car:
        car = Car(**car_data.dict())
        self.session.add(car)
        self.session.commit()
        self.session.refresh(car)
        return car

    def update(
        self, car_id: int, car_data: CarCreateSchema
    ) -> (
        Car | None
    ):  # car_data = CarCreateSchema, car_data.dict() = {'name':'fit', ...}, car_data.dict().items() = ('name', 'fit'), ('color', 'red')
        car = self.get_by_id(car_id)
        if not car:
            return None
        for key, value in car_data.dict().items():
            setattr(
                car, key, value
            )  # -> car.name = car_data.name, car.color = car_data.color, ...
        self.session.commit()
        return car

    def delete(self, car_id: int) -> dict | None:
        car = self.get_by_id(car_id)
        if not car:
            return None
        self.session.delete(car)
        self.session.commit()
        return {"message": "Car deleted successfully"}
