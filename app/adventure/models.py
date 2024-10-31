from app.database.database import Base
from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from enum import Enum


class AdventureState(Enum):
    not_ready = 0
    generating_text = 1
    image_adventure = 2
    image_items = 3
    image_characters = 4
    ready = 5


class AdventurePublic(BaseModel):
    id: int | None
    content: str | None


class Adventure(Base):
    __tablename__ = "adventure"

    id: Mapped[int | None] = mapped_column(primary_key=True, default=None)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"))
    content: Mapped[str | None] = mapped_column(default=None)
