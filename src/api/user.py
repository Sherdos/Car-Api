from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.apps.user.auth import create_access_token
from src.apps.user.schemas import UserBaseSchema


user_router = APIRouter()

users_db = {
    "user1": UserBaseSchema(username="user1", password="password1"),
    "user2": UserBaseSchema(username="user2", password="password2"),
}


@user_router.get("/", response_model=List[str])
def get_all_users() -> List[str]:
    return ["user1", "user2", "user3"]


@user_router.post("token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
