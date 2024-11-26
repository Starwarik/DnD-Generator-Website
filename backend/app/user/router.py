from fastapi import APIRouter, Depends

from typing_extensions import Annotated

from app.user.models import User
from app.auth.dependencies import get_current_user


user_router = APIRouter(tags=["user"])


@user_router.get("/api/user_info")
async def get_user_info(current_user: Annotated[User, Depends(get_current_user)]):
    return {
        "status": True,
        "username": current_user.username,
        "email": current_user.email,
        "balance": current_user.balance,
    }
