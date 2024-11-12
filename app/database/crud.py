from app.user.models import User
from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from app.generation.schemas import SpentedTokensCounts
from app.configs.generation import generation_setting

# READ method


def get_user_by_id(id: str, session: Session) -> User | None:
    statement = select(User).where(User.id == id)
    results = session.execute(statement)
    result = results.first()
    if result is None:
        return None
    return result[0]


def get_user_by_username(username: str, session: Session) -> User | None:
    statement = select(User).where(User.username == username)
    results = session.execute(statement)
    result = results.first()
    if result is None:
        return None
    return result[0]


def get_user_by_email(email: str, session: Session) -> User | None:
    statement = select(User).where(User.email == email)
    results = session.execute(statement)
    result = results.first()
    if result is None:
        return None
    return result[0]


def get_user_by_email_or_username(
    email_or_username: str, session: Session
) -> User | None:
    statement = select(User).where(
        or_(User.email == email_or_username, User.username == email_or_username)
    )
    results = session.execute(statement)
    result = results.first()
    if result is None:
        return None
    return result[0]


# CREATE method


def create_user(email: str, username: str, password_hash: str, session: Session):
    user = User(username=username, password=password_hash, email=email)
    session.add(user)
    session.commit()
    session.refresh(user)


# UPDATE method


def change_password(id: int, new_password_hash: str, session: Session):
    user = get_user_by_id(id, session)
    user.password = new_password_hash
    session.add(user)
    session.commit()
    session.refresh(user)


def change_balance_on_value(id: int, diff_balance: float, session: Session):
    user = get_user_by_id(id, session)
    user.balance += diff_balance
    session.add(user)
    session.commit()
    session.refresh(user)


def spend_balance_on_tokens(
    id: int, tokens_count: SpentedTokensCounts, session: Session
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
    change_balance_on_value(id, -diff_balance, session)
