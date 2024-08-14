from sqlmodel import Field, SQLModel


class Image(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(foreign_key="user.id")
    image: bytes
    media_type: str
