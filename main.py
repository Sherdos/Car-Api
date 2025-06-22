from typing import List
from fastapi import FastAPI, Depends

from sqlmodel import Session

from src.core.database import create_db_and_tables, get_session
from src.apps.car.schemas import CarCreateSchema, CarReadSchema
from src.apps.car.services import CarService

from src.api.cars import car_router
from src.api.user import user_router

# models -> repositories -> services -> routers

app = FastAPI(
    title="Car API",
    description="API for managing cars",
    version="0.0.1",
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(car_router, prefix="/api/cars", tags=["Cars"])
app.include_router(user_router, prefix="/api/users", tags=["Users"])
