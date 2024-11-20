from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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
