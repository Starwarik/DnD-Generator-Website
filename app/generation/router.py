from fastapi import APIRouter, Depends

from typing_extensions import Annotated

from app.database.table import User
from app.auth.dependencies import get_current_user

generation_router = APIRouter(tags=["generation"])


@generation_router.get("/api/generate")
def generate_adventure(current_user: Annotated[User, Depends(get_current_user)]):
    return {
        "status": True,
        "username": current_user.username,
        "email": current_user.email,
        "balance": current_user.balance,
    }
