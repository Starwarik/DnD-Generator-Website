from worker.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer, TypeDecorator, String
from enum import Enum


class AdventureState(Enum):
    """
    Хранит состояние генерации приключения

    0. not_ready - Не готово
    1. generating_text - Происходит генерация текста.
    2. image_adventure - Просиходит генерация обложки и карты приключения.
    3. image_items - Генерация картинок для предметов
    4. image_characters - Генерация картинок для персонажей
    5. ready - Приключение готово
    6. max_retry_error - Модель выдывала несколько раз подряд плохой результат. Ошибка
    7. censorship_error - Модель цензурирует запрос. Ошибка
    8. other_error - Ошибка другого рода
    """

    not_ready = 0
    generating_text = 1
    image_adventure = 2
    image_items = 3
    image_characters = 4
    ready = 5
    max_retry_error = 6
    censorship_error = 7
    other_error = 8


class IntEnum(TypeDecorator):
    """
    Нужен, чтобы хранить в бд Enum как int. Служебный класс.

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


class Adventure(Base):
    __tablename__ = "adventure"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    state: Mapped[AdventureState] = mapped_column(
        IntEnum(AdventureState), default=AdventureState.not_ready
    )
    content: Mapped[str] = mapped_column(default="{}")


class Image(Base):
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    image: Mapped[bytes]
    media_type: Mapped[str]


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    balance: Mapped[float] = mapped_column(default=0.0)

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, password={self.password!r}, balance={self.balance!r})"
