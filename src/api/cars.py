from typing import List, Optional
from fastapi import APIRouter, FastAPI, Depends, UploadFile

from sqlmodel import Session

from src.apps.user.auth import get_current_user
from src.core.database import create_db_and_tables, get_session
from src.apps.car.schemas import CarCreateSchema, CarReadSchema
from src.apps.car.services import CarService


car_router = APIRouter()


@car_router.get("", response_model=List[CarReadSchema])
def get_all_cars(
    mark_id: Optional[int] = None,
    session: Session = Depends(get_session),
) -> List[CarReadSchema]:
    cars = CarService(session).get_all_cars(mark_id)
    return [CarReadSchema.from_orm(car) for car in cars]


@car_router.get("/search", response_model=List[CarReadSchema])
def search_car(
    word: str, session: Session = Depends(get_session)
) -> List[CarReadSchema]:
    cars = CarService(session).search_car(word)
    return [CarReadSchema.from_orm(car) for car in cars]


@car_router.get("/{car_id}", response_model=CarReadSchema)
def get_car_by_id(
    car_id: int, session: Session = Depends(get_session)
) -> CarReadSchema:
    car = CarService(session).get_car(car_id)
    return CarReadSchema.from_orm(car)


@car_router.post("/", response_model=CarReadSchema)
def add_car(
    car: CarCreateSchema,
    session: Session = Depends(get_session),
    user_data: dict = Depends(get_current_user),
) -> CarReadSchema:
    new_car = CarService(session).create_car(
        user_data,
        car,
    )
    return CarReadSchema.from_orm(new_car)


@car_router.put("/{car_id}", response_model=CarReadSchema)
def edit_car(
    car_id: int,
    car: CarCreateSchema,
    session: Session = Depends(get_session),
    user_data: dict = Depends(get_current_user),
) -> CarReadSchema:
    print("User data:", user_data)
    updated_car = CarService(session).update_car(car_id, user_data, car)
    return CarReadSchema.from_orm(updated_car)


@car_router.delete(
    "/{car_id}",
    response_model=dict,
)
def delete_car(
    car_id: int,
    session: Session = Depends(get_session),
    user_data: dict = Depends(get_current_user),
) -> dict:
    message = CarService(session).delete_car(car_id, user_data)
    return message


@car_router.post("/upload-image", response_model=dict)
def image_upload(
    file: UploadFile,
    session: Session = Depends(get_session),
    user_data: dict = Depends(get_current_user),
) -> dict:

    return CarService(session).upload_image(file, user_data)
