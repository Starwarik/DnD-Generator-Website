from typing_extensions import Annotated
from fastapi import APIRouter, Depends

from app.user.models import User
from app.auth.dependencies import get_current_user
from app.payment.utils import *

payment_router = APIRouter(tags=["payment"])

@payment_router.post("/api/make_payment")
async def make_payment(current_user: Annotated[User, Depends(get_current_user)]):
    raise NotImplementedError()

@payment_router.post("/api/payment_success")
async def on_payment_success(current_user: Annotated[User, Depends(get_current_user)]):
    raise NotImplementedError()