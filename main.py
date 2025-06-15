from typing import List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlmodel import Session

from src.core.database import create_db_and_tables, get_session
from src.apps.car.models import Car
from src.apps.car.schemas import CarCreateSchema, CarReadSchema
from src.apps.car.services import CarService


# models -> repositories -> services -> routers

app = FastAPI(title="Car API", description="API for managing cars", version="0.0.1")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/cars", response_model=List[CarReadSchema])
def get_all_cars(session: Session = Depends(get_session)) -> List[CarReadSchema]:
    cars = session.query(Car).all()
    return cars


@app.get("/search", response_model=CarReadSchema)
def search_car(word: str, session: Session = Depends(get_session)) -> CarReadSchema:
    cars = session.query(Car).all()
    for car in cars:
        if word in car.name:
            return car
    raise HTTPException(404, "Car not found")


@app.get("/cars/{car_id}", response_model=CarReadSchema)
def get_car_by_id(
    car_id: int, session: Session = Depends(get_session)
) -> CarReadSchema:
    car = CarService(session).get_car(car_id)
    return car


@app.post("/cars/", response_model=CarReadSchema)
def add_car(
    car: CarCreateSchema, session: Session = Depends(get_session)
) -> CarReadSchema:
    new_car = CarService(session).create_car(car)
    return new_car


@app.put("/cars/{car_id}", response_model=CarReadSchema)
def edit_car(
    car_id: int, car: CarCreateSchema, session: Session = Depends(get_session)
) -> CarReadSchema:
    updated_car = CarService(session).update_car(car_id, car)
    return updated_car


@app.delete("/cars/{car_id}", response_model=dict)
def delete_car(car_id: int, session: Session = Depends(get_session)) -> dict:
    message = CarService(session).delete_car(car_id)
    return message
