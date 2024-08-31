from sqlmodel import Field, SQLModel
from enum import Enum

from app.adventure.schemas import AdventureInfo


class AdventureState(Enum):
    not_ready = 0
    generating_text = 1
    image_adventure = 2
    image_items = 3
    image_characters = 4
    ready = 5


class AdventurePublic(SQLModel):
    id: int | None
    state: AdventureState
    content: AdventureInfo | None


class Adventure(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(foreign_key="user.id")
    state: AdventureState = Field(default=AdventureState.not_ready)
    content: str | None = Field(default=None)
