from sqlmodel import Field, SQLModel
from enum import Enum


class AdventureState(Enum):
    not_ready = 0
    ready = 1


class Adventure(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(foreign_key="user.id")
    state: AdventureState = Field(default=AdventureState.not_ready)
    content: str | None = Field(default=None)
