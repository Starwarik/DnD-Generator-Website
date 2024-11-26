from app.user.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.generation.schemas import SpentedTokensCounts
from app.generation.config import generation_setting

# READ method


async def get_user_by_id(id: str, session: AsyncSession) -> User | None:
    statement = select(User).where(User.id == id)
    results = await session.execute(statement)
    result = results.scalars().first()
    if result is None:
        return None
    return result


async def get_user_by_username(username: str, session: AsyncSession) -> User | None:
    statement = select(User).where(User.username == username)
    results = await session.execute(statement)
    result = results.scalars().first()
    if result is None:
        return None
    return result


async def get_user_by_email(email: str, session: AsyncSession) -> User | None:
    statement = select(User).where(User.email == email)
    results = await session.execute(statement)
    result = results.scalars().first()
    if result is None:
        return None
    return result


async def get_user_by_email_or_username(
    email_or_username: str, session: AsyncSession
) -> User | None:
    statement = select(User).where(
        or_(User.email == email_or_username, User.username == email_or_username)
    )
    results = await session.execute(statement)
    result = results.scalars().first()
    if result is None:
        return None
    return result


# CREATE method


async def create_user(
    email: str, username: str, password_hash: str, session: AsyncSession
):
    async with session.begin():
        user = User(username=username, password=password_hash, email=email)
        session.add(user)


# UPDATE method


async def change_password(id: int, new_password_hash: str, session: AsyncSession):
    async with session.begin():
        user = await get_user_by_id(id, session)
        user.password = new_password_hash
        session.add(user)


async def change_balance_on_value(id: int, diff_balance: float, session: AsyncSession):
    async with session.begin():
        user = await get_user_by_id(id, session)
        user.balance += diff_balance
        session.add(user)


async def spend_balance_on_tokens(
    id: int, tokens_count: SpentedTokensCounts, session: AsyncSession
):
    diff_balance = (
        tokens_count.gigachat_assistant_token_count
        * generation_setting.gigachat_assistant_token_cost
        + tokens_count.gigachat_prompt_token_count
        * generation_setting.gigachat_prompt_token_cost
        + tokens_count.yandexgpt_assistant_token_count
        * generation_setting.yandexgpt_assistant_token_cost
        + tokens_count.yandexgpt_prompt_token_count
        * generation_setting.yandexgpt_prompt_token_cost
        + tokens_count.image_generated * generation_setting.image_generated_cost
    )
    await change_balance_on_value(id, -diff_balance, session)
