from app.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class Image(Base):
    id: Mapped[int | None] = mapped_column(primary_key=True, default=None)
    user_id: Mapped[int | None] = mapped_column(ForeignKey=("user.id"))
    image: Mapped[bytes]
    media_type: Mapped[str]

