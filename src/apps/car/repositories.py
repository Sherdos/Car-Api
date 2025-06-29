from sqlmodel import Session
from src.apps.user.models import User
from src.apps.car.models import Car
from src.apps.car.schemas import CarCreateSchema


class CarRepository:
    def __init__(self, session: Session):
        self.session: Session = session

    def get_all(self, mark: int = None) -> list[Car]:
        if mark:
            return self.session.query(Car).filter(Car.mark_id == mark).all()
        return self.session.query(Car).all()

    def get_by_id(self, car_id: int) -> Car | None:
        return self.session.query(Car).filter(Car.id == car_id).first()

    def create(self, username: str, car_data: CarCreateSchema) -> Car:
        user_id = self.session.query(User).filter(User.username == username).first().id
        car = Car(**car_data.dict(), user_id=user_id)
        self.session.add(car)
        self.session.commit()
        self.session.refresh(car)
        return car

    def update(self, user_data, car_id: int, car_data: CarCreateSchema) -> Car | dict:
        user_id = self.session.query(User).filter(User.username == user_data).first().id
        car = self.get_by_id(car_id)
        if not car:
            return {"message": "Car not found"}
        if car.user_id != user_id:
            return {"message": "You are not authorized to update this car"}
        for key, value in car_data.dict().items():
            setattr(car, key, value)
        self.session.commit()
        return car

    def delete(self, car_id: int) -> dict | None:
        car = self.get_by_id(car_id)
        if not car:
            return None
        self.session.delete(car)
        self.session.commit()
        return {"message": "Car deleted successfully"}

    def search(self, word: str) -> list[Car]:
        cars = self.session.query(Car).all()
        found_cars = [car for car in cars if word.lower() in car.name.lower()]
        return found_cars
