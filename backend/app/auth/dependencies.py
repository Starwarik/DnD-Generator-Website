from typing_extensions import Annotated
from fastapi import Depends, HTTPException, status

from app.database.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.user.models import User
from .utils import jwt_decode, get_user_by_id


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"status": False},
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt_decode(token)
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user_by_id(user_id, session)
    if user is None:
        raise credentials_exception
    return user
