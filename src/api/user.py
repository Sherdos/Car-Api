from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from src.apps.user.repositories import UserRepository
from src.apps.user.serveces import UserService
from src.apps.user.auth import create_access_token
from src.apps.user.schemas import UserBaseSchema, UserCreateSchema

from src.core.database import create_db_and_tables, get_session

user_router = APIRouter()

# users_db = {
#     "user1": UserBaseSchema(username="user1", password="password1"),
#     "user2": UserBaseSchema(username="user2", password="password2"),
# }


@user_router.get("/", response_model=List[str])
def get_all_users() -> List[str]:
    return ["user1", "user2", "user3"]


@user_router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_session),
):
    service = UserService(db_session=db_session)
    user = service.login_user(username=form_data.username, password=form_data.password)

    access_token = create_access_token(user.dict())
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/register", response_model=UserBaseSchema)
def register_user(user: UserCreateSchema, db_session: Session = Depends(get_session)):
    service = UserService(db_session=db_session)
    return service.create_user(user)
