from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.adventure.models import Adventure, AdventureState
from app.adventure.schemas import AdventureInfo


async def create_adventure(user_id: int, session: AsyncSession) -> Adventure:
    adventure = Adventure(user_id=user_id, state=AdventureState.generating_text)
    session.add(adventure)
    await session.commit()
    await session.refresh(adventure)
    return adventure


async def get_adventure(
    id: int,
    user_id: int,
    session: AsyncSession,
) -> Adventure:
    command = select(Adventure).where(Adventure.id == id, Adventure.user_id == user_id)
    results = await session.execute(command)
    result = results.scalars().first()
    if result is None:
        raise Exception()
    return result


async def update_state_content_adventure(
    id: int,
    state: AdventureState | None,
    content: AdventureInfo | None,
    session: AsyncSession,
) -> Adventure:
    new_values = {}
    if state:
        new_values["state"] = state
    if content:
        new_values["content"] = content.model_dump_json()

    async with session.begin():
        command = (
            update(Adventure)
            .where(Adventure.id == id)
            .values(**new_values)
            .returning(Adventure)
        )
        results = await session.execute(command)
        result = results.scalars().one()
    return result
