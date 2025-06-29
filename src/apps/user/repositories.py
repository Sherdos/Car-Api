from src.apps.user.models import User
from sqlmodel import Session


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    """

    data -> add() -> database_copy -> commit() -> database
    database -> refresh() -> data
    """

    def create_user(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user_by_id(self, user_id: int):
        return self.session.get(User, user_id)

    def get_user_by_username(self, username: str) -> User | None:
        return self.session.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> User | None:
        return self.session.query(User).filter(User.email == email).first()

    def update_user(self, user: User):
        self.session.merge(user)
        self.session.commit()
        return user

    def delete_user(self, user: User):
        self.session.delete(user)
        self.session.commit()

    def login_user(self, username: str, password: str):
        user = self.get_user_by_username(username)

        if user and user.password == password:
            return user
        return None
