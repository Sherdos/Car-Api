from typing import List
from fastapi import APIRouter, Depends


user_router = APIRouter()


@user_router.get("/", response_model=List[str])
def get_all_users() -> List[str]:
    return ["user1", "user2", "user3"]
