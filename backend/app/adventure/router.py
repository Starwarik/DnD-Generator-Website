from fastapi import APIRouter, Depends, HTTPException, Response

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from typing_extensions import Annotated

from app.adventure.schemas import AdventureInfo
from app.adventure.service import (
    update_state_content_adventure,
)
from app.database.database import get_session
from app.adventure.models import Adventure, AdventurePublic, AdventureState
from app.user.models import User
from app.auth.dependencies import get_current_user

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
        new_values["content "] = content.model_dump_json()
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
    stmt = delete(Adventure).where(
        (Adventure.id == adventure_id) & (Adventure.user_id == current_user.id)
    )
    await session.execute(stmt)
    await session.commit()
    return Response(status_code=200)


@adventure_router.post(
    "/api/adventure/{id_adventure}/annotation", response_model=AdventurePublic
)
async def change_annotation(
    id_adventure: int,
    new_annotation: str,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    command = select(Adventure).where(
        Adventure.user_id == current_user.id, Adventure.id == id_adventure
    )
    results = await session.execute(command)
    adventure = results.scalars().first()
    content = AdventureInfo.model_validate_json(adventure.content)
    content.annotation = new_annotation
    adventure = await update_state_content_adventure(
        adventure.id, AdventureState.ready, content, session
    )
    return adventure
