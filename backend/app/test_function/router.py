from typing import Annotated
from fastapi import APIRouter, Depends

from app.user.models import User
from app.database.database import get_session

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.adventure.models import Adventure
from app.adventure.schemas import AdventureInfo
from app.auth.dependencies import get_current_user

test_router = APIRouter(tags=["test_function"])


@test_router.get("/api/get_users")
async def get_all_users(session: AsyncSession = Depends(get_session)):
    statement = select(User)
    results = await session.execute(statement)
    result = results.scalars().all()
    return result


@test_router.post("/api/infinite_money/{user_id}")
async def get_infinite_money(
    user_id: int, session: AsyncSession = Depends(get_session)
):
    async with session.begin():
        statement = (
            update(User)
            .where(User.id == user_id)
            .values(balance=99999999999999999999999999)
        )
        await session.execute(statement)


@test_router.get("/api/adventure_more/{adventure_id}")
async def get_adventure(
    current_user: Annotated[User, Depends(get_current_user)],
    adventure_id: int,
    session: AsyncSession = Depends(get_session),
):
    result = await session.get(Adventure, adventure_id)
    if result is None or result.user_id != current_user.id:
        raise Exception()
    return AdventureInfo.model_validate_json(result.content).model_dump()
