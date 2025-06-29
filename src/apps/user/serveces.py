from fastapi import HTTPException, status
from src.apps.user.models import User
from src.apps.user.schemas import UserCreateSchema, UserUpdateSchema
from src.apps.user.repositories import UserRepository


class UserService:
    def __init__(self, db_session):
        self.db_session = db_session
        self.repository = UserRepository(db_session)

    def create_user(self, user: UserCreateSchema):
        user_data = User(**user.dict())  # type: ignore
        new_user = self.repository.create_user(user_data)
        return new_user

    def get_user_by_id(self, user_id):
        return self.repository.get_user_by_id(user_id)

    def get_user_by_username(self, username):
        return self.repository.get_user_by_username(username)

    def get_user_by_email(self, email):
        return self.repository.get_user_by_email(email)

    def update_user(self, user_id, user: UserUpdateSchema):
        old_user = self.repository.get_user_by_id(user_id)
        updated_data = old_user.update(**user.dict(exclude_unset=True))  # type: ignore
        updated_user = self.repository.update_user(updated_data)
        return updated_user

    def login_user(self, username: str, password: str):
        user = self.repository.login_user(username, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
