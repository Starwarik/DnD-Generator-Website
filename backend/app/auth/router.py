from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.database.database import get_session
from app.database.crud import *
from app.notification.notifications import notification_service
from app.auth.utils import *
from app.auth.config import auth_setting

from pydantic import BaseModel

from typing_extensions import Annotated

from jwt.exceptions import InvalidTokenError


class RestPasswordForm(BaseModel):
    new_password: str
    token_reset: str


class Token(BaseModel):
    status: bool = True
    access_token: str
    token_type: str


class UserRegisterForm(BaseModel):
    username: str
    password: str
    email: str


auth_router = APIRouter(tags=["auth"])


@auth_router.post("/token")
@auth_router.post("/api/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": False},
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_setting.token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.get("/api/reset_token")
async def reset_token(email: str, session: AsyncSession = Depends(get_session)) -> None:
    user = await get_user_by_email(email, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"status": False},
            headers={"WWW-Authenticate": "Bearer"},
        )
    reset_token_expires = timedelta(minutes=auth_setting.token_expire_minutes)
    reset_token = create_access_token(
        data={"sub": user.id, "type": "reset"}, expires_delta=reset_token_expires
    )
    notification_service.send_refactory_notification(user.email, reset_token)


@auth_router.post("/api/register")
async def register(
    user: UserRegisterForm, session: AsyncSession = Depends(get_session)
):
    user_username = await get_user_by_username(user.username, session)
    user_email = await get_user_by_email(user.email, session)
    current_user = user_username or user_email
    if not (current_user is None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"status": False},
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        await create_user(
            email=user.email,
            username=user.username,
            password_hash=get_password_hash(user.password),
            session=session,
        )
        return {"status": True}
    except Exception as e:
        print(e)
        return {"status": False}


@auth_router.post("/api/reset_password")
async def reset_password(
    reset_form: RestPasswordForm, session: AsyncSession = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"status": False},
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt_decode(reset_form.token_reset)
        user_id: str | None = payload.get("sub")
        if user_id is None or payload.get("type") != "reset":
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    # if user is None:
    #    raise credentials_exception
    await change_password(
        int(user_id), get_password_hash(reset_form.new_password), session
    )
    return {"status": True}
