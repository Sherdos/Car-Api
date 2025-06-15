from typing import List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlmodel import Session

from src.core.database import create_db_and_tables, get_session
from src.apps.car.models import Car
from src.apps.car.schemas import CarCreateSchema, CarReadSchema


app = FastAPI()


def get_by_id(session: Session, car_id: int) -> Car:
    try:
        return session.query(Car).filter(Car.id == car_id).one()
    except:
        raise HTTPException(404, "Car not found")


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
    car = get_by_id(session, car_id)
    return car


@app.post("/cars/", response_model=CarReadSchema)
def add_car(
    car: CarCreateSchema, session: Session = Depends(get_session)
) -> CarReadSchema:
    new_car = Car(name=car.name, color=car.color, mark=car.mark)
    session.add(new_car)
    session.commit()
    return new_car


@app.put("/cars/{car_id}", response_model=List[CarReadSchema])
def edit_car(
    car_id: int, car: CarReadSchema, session: Session = Depends(get_session)
) -> List[CarReadSchema]:
    exist_car = get_by_id(session, car_id)
    exist_car.name = car.name
    exist_car.color = car.color
    exist_car.mark = car.mark
    session.add(exist_car)
    session.commit()
    cars = session.query(Car).all()
    return cars


@app.delete("/cars/{car_id}", response_model=dict)
def delete_car(car_id: int, session: Session = Depends(get_session)) -> dict:
    stmt = delete(Car).where(Car.id == car_id)
    session.execute(stmt)
    session.commit()
    return {"message": "Car deleted successfully"}
