import jwt
import bcrypt

from typing import Union

from datetime import datetime, timedelta, timezone

from app.payment.config import payment_setting
from app.database.crud import *


def jwt_encode(content):
    return jwt.encode(
        content, payment_setting.secret_key_jwt, algorithm=payment_setting.algorithm_jwt
    )


def jwt_decode(content):
    return jwt.decode(
        content, payment_setting.secret_key_jwt, algorithms=[payment_setting.algorithm_jwt]
    )


def create_payment_token(user_id: int, amount: float, expires_delta: Union[timedelta, None] = None):
    to_encode = {
        "amount": amount,
        "user_id": user_id
    }
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt_encode(to_encode)
    return encoded_jwt
