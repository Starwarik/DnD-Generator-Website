from sqlalchemy import String
from app.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    balance: Mapped[float] = mapped_column(default=0.0)

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, password={self.password!r}, balance={self.balance!r})"
