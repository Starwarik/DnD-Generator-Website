from app.database.database import Base
from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer, TypeDecorator
from enum import Enum


class AdventureState(Enum):
    not_ready = 0
    generating_text = 1
    image_adventure = 2
    image_items = 3
    image_characters = 4
    ready = 5


class IntEnum(TypeDecorator):
    """
    Enables passing in a Python enum and storing the enum's *value* in the db.
    The default would have stored the enum's *name* (ie the string).
    """

    impl = Integer

    def __init__(self, enumtype, *args, **kwargs):
        super(IntEnum, self).__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, int):
            return value

        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)


class AdventurePublic(BaseModel):
    id: int | None
    content: str | None


class Adventure(Base):
    __tablename__ = "adventure"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    state: Mapped[AdventureState] = mapped_column(IntEnum(AdventureState))
    content: Mapped[str | None] = mapped_column(default=None)
