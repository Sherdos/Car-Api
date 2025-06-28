from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # первичный ключ
    username: str = Field(default="", unique=True, index=True)
    email: str = Field(default="", unique=True, index=True)
    password: str = Field(default="")

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"
