from sqlmodel import Field, SQLModel
from sqlalchemy.sql.schema import Column
from sqlalchemy import String


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column("username", String, unique=True))
    password: str
    email: str = Field(sa_column=Column("email", String, unique=True))
    balance: float = Field(default=0.0)
