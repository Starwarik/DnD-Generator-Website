from fastapi import APIRouter, Depends, HTTPException, status

from typing_extensions import Annotated

from app.database.table import User
from app.database.database import get_session
from app.auth.dependencies import get_current_user

from sqlmodel import Session

from app.database.crud import change_balance_on_value

user_router = APIRouter(tags=["user"])


@user_router.get("/api/user_info", tags=["user"])
def get_user_info(current_user: Annotated[User, Depends(get_current_user)]):
    return {
        "status": True,
        "username": current_user.username,
        "email": current_user.email,
        "balance": current_user.balance,
    }


@user_router.post("/api/spend_balance", tags=["user"])
def spend_balance(
    money: float,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
) -> float:
    if money < 0:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail={"status": False},
            headers={"WWW-Authenticate": "Bearer"},
        )
    if money - current_user.balance > 0:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={"status": False},
            headers={"WWW-Authenticate": "Bearer"},
        )
    change_balance_on_value(current_user.id, -money, session)
    return current_user.balance - money


"""
Debug function

@user_router.get("/api/get_users")
def get_all_users(session: Session = Depends(get_session)):
    statement = select(User)
    results = session.exec(statement)
    result = results.all()
    return result
"""
