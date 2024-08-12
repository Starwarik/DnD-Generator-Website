from .table import User
from sqlmodel import Session, select, or_

# READ method


def get_user_by_id(id: str, session: Session) -> User | None:
    statement = select(User).where(User.id == id)
    results = session.exec(statement)
    result = results.first()
    return result


def get_user_by_username(username: str, session: Session) -> User | None:
    statement = select(User).where(User.username == username)
    results = session.exec(statement)
    result = results.first()
    return result


def get_user_by_email(email: str, session: Session) -> User | None:
    statement = select(User).where(User.email == email)
    results = session.exec(statement)
    result = results.first()
    return result


def get_user_by_email_or_username(
    email_or_username: str, session: Session
) -> User | None:
    statement = select(User).where(
        or_(User.email == email_or_username, User.username == email_or_username)
    )
    results = session.exec(statement)
    result = results.first()
    return result


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


def change_balance_on_value(id: int, balance: int, session: Session):
    user = get_user_by_id(id, session)
    user.balance += balance
    session.add(user)
    session.commit()
    session.refresh(user)
