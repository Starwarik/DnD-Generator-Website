from sqlalchemy.sql.schema import Column
from sqlalchemy import String
from app.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "user"

    id: Mapped[int | None] = mapped_column(primary_key=True, default=None)
    username = Column("username", String, unique=True, index=True)
    password: Mapped[str]
    email = Column("email", String, unique=True, index=True)
    balance: Mapped[float] = mapped_column(default=0.0)
