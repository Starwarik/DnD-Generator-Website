import jwt
import bcrypt

from typing import Union

from datetime import datetime, timedelta, timezone

from .config import auth_setting
from app.database.crud import *


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def jwt_encode(content):
    return jwt.encode(
        content, auth_setting.secret_key_jwt, algorithm=auth_setting.algorithm_jwt
    )


def jwt_decode(content):
    return jwt.decode(
        content, auth_setting.secret_key_jwt, algorithms=[auth_setting.algorithm_jwt]
    )


def authenticate_user(
    username_or_email: str, password: str, session: Session
) -> User | None:
    user = get_user_by_email_or_username(username_or_email, session)
    print(user)
    if user is None:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt_encode(to_encode)
    return encoded_jwt
