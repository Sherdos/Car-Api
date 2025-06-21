from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, Query

from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlmodel import Session

from src.core.database import create_db_and_tables, get_session
from src.apps.car.models import Car
from src.apps.car.schemas import CarCreateSchema, CarReadSchema
from src.apps.car.services import CarService


# models -> repositories -> services -> routers

app = FastAPI(
    title="Car API",
    description="API for managing cars",
    version="0.0.1",
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/cars", response_model=List[CarReadSchema], tags=["Cars"])
def get_all_cars(
    mark: int, session: Session = Depends(get_session)
) -> List[CarReadSchema]:
    cars = CarService(session).get_all_cars(mark)
    return cars


@app.get("/search", response_model=List[CarReadSchema], tags=["Cars"])
def search_car(word: str, session: Session = Depends(get_session)) -> CarReadSchema:
    cars = CarService(session).search_car(word)
    return cars


@app.get("/cars/{car_id}", response_model=CarReadSchema, tags=["Cars"])
def get_car_by_id(
    car_id: int, session: Session = Depends(get_session)
) -> CarReadSchema:
    car = CarService(session).get_car(car_id)
    return car


@app.post("/cars/", response_model=CarReadSchema, tags=["Cars"])
def add_car(
    car: CarCreateSchema, session: Session = Depends(get_session)
) -> CarReadSchema:
    new_car = CarService(session).create_car(car)
    return new_car


@app.put("/cars/{car_id}", response_model=CarReadSchema, tags=["Cars"])
def edit_car(
    car_id: int, car: CarCreateSchema, session: Session = Depends(get_session)
) -> CarReadSchema:
    updated_car = CarService(session).update_car(car_id, car)
    return updated_car


@app.delete("/cars/{car_id}", response_model=dict, tags=["Cars"])
def delete_car(car_id: int, session: Session = Depends(get_session)) -> dict:
    message = CarService(session).delete_car(car_id)
    return message
