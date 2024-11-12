from fastapi import APIRouter, Depends, HTTPException, status

from typing_extensions import Annotated

from app.user.models import User
from app.database.database import get_session
from app.auth.dependencies import get_current_user

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.configs.app import app_setting


user_router = APIRouter(tags=["user"])


@user_router.get("/api/user_info")
def get_user_info(current_user: Annotated[User, Depends(get_current_user)]):
    return {
        "status": True,
        "username": current_user.username,
        "email": current_user.email,
        "balance": current_user.balance,
    }


if app_setting.is_test:

    @user_router.get("/api/get_users")
    def get_all_users(session: Session = Depends(get_session)):
        statement = select(User)
        results = session.execute(statement)
        result = results.scalars().all()
        return result

    @user_router.post("/api/infinite_money/{user_id}")
    def get_infinite_money(user_id: int, session: Session = Depends(get_session)):
        statement = (
            update(User)
            .where(User.id == user_id)
            .values(balance=99999999999999999999999999)
        )
        session.execute(statement)
        session.commit()
