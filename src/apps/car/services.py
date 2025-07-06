from typing import Optional
from sqlmodel import Session
from fastapi import HTTPException, UploadFile, status

from random import randint

from src.apps.car.models import Car
from src.apps.car.repositories import CarRepository
from src.apps.car.schemas import CarCreateSchema


class CarService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = CarRepository(session)

    def get_all_cars(self, mark_id: Optional[int] = None) -> list[Car]:
        cars = self.repository.get_all(mark_id)
        return cars

    def create_car(self, user_data: dict, car_data: CarCreateSchema) -> Car:
        car = self.repository.create(user_data["id"], car_data)
        return car

    def get_car(self, car_id) -> Car | None:
        car = self.repository.get_by_id(car_id)
        if car == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return car

    def update_car(
        self, car_id: int, user_data: dict, car_data: CarCreateSchema
    ) -> Car:

        car = self.repository.update(user_data["id"], car_id, car_data)
        if type(car) is dict:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=car.get("message")
            )
        return car

    def delete_car(self, car_id: int, user_data: dict) -> dict:
        message = self.repository.delete(car_id, user_data["id"])
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

    def upload_image(self, file: UploadFile, user_data: dict) -> dict:
        if not file:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided"
            )

        file_path = f"media/{randint(1, 10000)}_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        return {"message": "Image uploaded successfully", "file_path": file_path}
