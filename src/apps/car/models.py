from sqlmodel import Field, SQLModel, create_engine, Session, delete, select


class Car(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default="")
    color: str = Field(default="white")
    mark_id: int = Field(
        default=None, foreign_key="mark.id"
    )  # Foreign key to Mark table
    user_id: int = Field(
        default=None, foreign_key="user.id"
    )  # Foreign key to User table


class Mark(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # unique
    name: str = Field(default="", unique=True)  # unique name for each mark
