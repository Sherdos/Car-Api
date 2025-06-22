from typing import List
from fastapi import APIRouter, FastAPI, Depends

from sqlmodel import Session

from src.core.database import create_db_and_tables, get_session
from src.apps.car.schemas import CarCreateSchema, CarReadSchema
from src.apps.car.services import CarService


car_router = APIRouter()


@car_router.get("", response_model=List[CarReadSchema])
def get_all_cars(
    mark: int = None, session: Session = Depends(get_session)
) -> List[CarReadSchema]:
    cars = CarService(session).get_all_cars(mark)
    return cars


@car_router.get("/search", response_model=List[CarReadSchema])
def search_car(word: str, session: Session = Depends(get_session)) -> CarReadSchema:
    cars = CarService(session).search_car(word)
    return cars


@car_router.get("/{car_id}", response_model=CarReadSchema)
def get_car_by_id(
    car_id: int, session: Session = Depends(get_session)
) -> CarReadSchema:
    car = CarService(session).get_car(car_id)
    return car


@car_router.post("/", response_model=CarReadSchema)
def add_car(
    car: CarCreateSchema, session: Session = Depends(get_session)
) -> CarReadSchema:
    new_car = CarService(session).create_car(car)
    return new_car


@car_router.put("/{car_id}", response_model=CarReadSchema)
def edit_car(
    car_id: int, car: CarCreateSchema, session: Session = Depends(get_session)
) -> CarReadSchema:
    updated_car = CarService(session).update_car(car_id, car)
    return updated_car


@car_router.delete("/{car_id}", response_model=dict)
def delete_car(car_id: int, session: Session = Depends(get_session)) -> dict:
    message = CarService(session).delete_car(car_id)
    return message
