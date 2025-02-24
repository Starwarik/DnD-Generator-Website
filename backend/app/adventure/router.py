from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from typing_extensions import Annotated

from app.adventure.schemas import AdventureInfo
from app.database.database import get_session
from app.adventure.models import Adventure, AdventurePublic, AdventureState
from app.user.models import User
from app.auth.dependencies import get_current_user
from app.image.models import Image

adventure_router = APIRouter(tags=["adventure"])


@adventure_router.get("/api/adventure", response_model=list[AdventurePublic])
async def get_user_adventures(
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    command = select(Adventure).where(Adventure.user_id == current_user.id)
    results = await session.execute(command)
    results = results.scalars().all()
    return results


@adventure_router.get("/api/adventure/{adventure_id}", response_model=AdventurePublic)
async def get_adventure(
    current_user: Annotated[User, Depends(get_current_user)],
    adventure_id: int,
    session: AsyncSession = Depends(get_session),
):
    result = await session.get(Adventure, adventure_id)
    if result is None or result.user_id != current_user.id:
        raise Exception()
    return result


@adventure_router.put("/api/adventure/{id_adventure}", response_model=None)
async def update_adventure(
    id_adventure: int,
    content: AdventureInfo,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
) -> Adventure:
    new_values = {}

    adventure = await session.get(Adventure, id_adventure)
    if adventure is None:
        raise HTTPException(status_code=404, detail="Adventure not found")

    if adventure.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this adventure"
        )

    if adventure.state == AdventureState.ready:
        new_values["content"] = content.model_dump_json()
    else:
        raise HTTPException(status_code=403, detail="Adventure is not ready for update")

    if not new_values:
        raise HTTPException(status_code=400, detail="No fields to update")

    try:
        command = (
            update(Adventure).where(Adventure.id == id_adventure).values(**new_values)
        )
        await session.execute(command)
        await session.commit()

        result = await session.get(Adventure, id_adventure)

        if result is None:
            raise HTTPException(status_code=404, detail="Adventure not found")

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    return result


@adventure_router.delete(
    "/api/adventure/{adventure_id}",
    response_model=AdventurePublic,
    responses={200: {"model": None}},
)
async def delete_adventure(
    current_user: Annotated[User, Depends(get_current_user)],
    adventure_id: int,
    session: AsyncSession = Depends(get_session),
):
    adventure = await session.get(Adventure, adventure_id)
    if adventure is None:
        raise HTTPException(status_code=404, detail="Adventure not found")

    if adventure.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this adventure"
        )
    
    content = AdventureInfo.model_validate(adventure.content)

    images_ids: list[int] = []
    images_ids.append(content.adventure_image_id)
    images_ids.append(content.map_image_id)
    images_ids.extend([item.image_id for item in content.items])
    images_ids.extend([npc.image_id for npc in content.npcs])
    images_ids = list(filter(lambda x: x != -1 and x != -42, images_ids))

    if len(images_ids) != 0:
        command = delete(Image).where(Image.id.in_(images_ids))
        await session.execute(command)
        await session.commit()

    command = delete(Adventure).where(Adventure.id == id) # type: ignore
    await session.execute(command)
    await session.commit()
