from sqlmodel import Session
from fastapi import HTTPException, status

from src.apps.car.models import Car
from src.apps.car.repositories import CarRepository
from src.apps.car.schemas import CarCreateSchema


class CarService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = CarRepository(session)

    def create_car(self, car_data: CarCreateSchema) -> Car:
        car = self.repository.create(car_data)
        return car

    def get_car(self, car_id) -> Car | None:
        car = self.repository.get_by_id(car_id)
        if car == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return car

    def update_car(self, car_id: int, car_data: CarCreateSchema) -> Car | None:
        car = self.repository.update(car_id, car_data)
        if car == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return car

    def delete_car(self, car_id: int) -> dict:
        message = self.repository.delete(car_id)
        if message == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return message
