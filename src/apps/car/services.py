from sqlmodel import Session
from fastapi import HTTPException, status

from src.apps.car.models import Car
from src.apps.car.repositories import CarRepository
from src.apps.car.schemas import CarCreateSchema


class CarService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = CarRepository(session)

    def get_all_cars(self, mark_id: int) -> list[Car]:
        cars = self.repository.get_all(mark_id)
        return cars

    def create_car(self, username: str, car_data: CarCreateSchema) -> Car:
        car = self.repository.create(username, car_data)
        return car

    def get_car(self, car_id) -> Car | None:
        car = self.repository.get_by_id(car_id)
        if car == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return car

    def update_car(
        self, car_id: int, user_data: dict, car_data: CarCreateSchema
    ) -> Car:

        car = self.repository.update(user_data, car_id, car_data)
        if type(car) is dict:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=car.get("message")
            )
        return car

    def delete_car(self, car_id: int) -> dict:
        message = self.repository.delete(car_id)
        if message == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return message

    def search_car(self, word: str) -> list[Car]:
        cars = self.repository.search(word)
        if not cars:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"
            )
        return cars
