from fastapi import APIRouter, Depends

from app.user.models import User
from app.database.database import get_session

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

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
