from base64 import b64decode, b64encode

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.image.models import Image
from app.image.schemas import ImageContainer


async def upload_image(
    container: ImageContainer, user_id: int, session: AsyncSession
) -> Image:
    image = Image(
        image=container.content, media_type=container.media_type, user_id=user_id
    )
    session.add(image)
    await session.commit()
    await session.refresh(image)
    return image


async def get_image_by_id(
    image_id: int, user_id: int, session: AsyncSession
) -> Image | None:
    command = select(Image).where(Image.user_id == user_id, Image.id == image_id)
    results = await session.execute(command)
    result = results.scalars().first()
    if result is None:
        return None
    return result
