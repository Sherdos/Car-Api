from sqlmodel import Field, SQLModel, create_engine, Session, delete, select


class Car(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default="")
    color: str = Field(default="white")
    mark_id: int = Field(
        default=None, foreign_key="mark.id"
    )  # Foreign key to Mark table


class Mark(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)  # unique
    name: str = Field(default="", unique=True)  # unique name for each mark

    """
     id | name | color | mark
    ----|------|-------|------
    1  | Audi | red   | tesla
    2  | BMW  | blue  | honda
    3  | Tesla| white | hodai
    
    Car table example:
    id | name | color | mark_id
    ----|------|-------|------
    1  | ModelX | red  | 1
    2  | BMW  | blue  | 2
    3  | Tesla| white | 3
    4  | Honda| black | 1
    
    
    Mark table example:
    id | name
    ----|------
    1  | Tesla
    2  | Honda
    3  | BMW
    4  | Audi
    
    
    
    """
