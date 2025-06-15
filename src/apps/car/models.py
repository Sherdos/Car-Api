from sqlmodel import Field, SQLModel, create_engine, Session, delete, select


class Car(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default="")
    color: str = Field(default="white")
    mark: str = Field(default="")
