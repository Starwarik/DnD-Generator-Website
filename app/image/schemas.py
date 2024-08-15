from pydantic import BaseModel


class ImageContainer(BaseModel):
    content: bytes
    media_type: str
