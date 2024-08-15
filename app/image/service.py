from base64 import b64decode, b64encode

from sqlmodel import Session, select

from app.image.models import Image
from app.image.schemas import ImageContainer


def upload_image(container: ImageContainer, user_id: int, session: Session):
    image = Image(
        image=container.content, media_type=container.media_type, user_id=user_id
    )
    session.add(image)
    session.commit()
    session.refresh(image)


def get_image_by_id(image_id: int, user_id: int, session: Session) -> Image | None:
    command = select(Image).where(Image.user_id == user_id).where(Image.id == image_id)
    results = session.exec(command)
    return results.first()
