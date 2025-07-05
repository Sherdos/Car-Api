from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session

from src.api.cars import car_router
from src.api.user import user_router
from src.core.database import create_db_and_tables

# models -> repositories -> services -> routers

app = FastAPI(
    title="Car API",
    description="API for managing cars",
    version="0.0.1",
)
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):

    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )


@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context={"title": "Home"}
    )


@app.get("/about", response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse(
        request=request, name="about.html", context={"title": "About"}
    )


@app.get("/create", response_class=HTMLResponse)
async def read_create(request: Request):
    return templates.TemplateResponse(
        request=request, name="create.html", context={"title": "Create Car"}
    )


# about

# create car

app.include_router(car_router, prefix="/api/cars", tags=["Cars"])
app.include_router(user_router, prefix="/api/users", tags=["Users"])
