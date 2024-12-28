from typing_extensions import Annotated
from fastapi import APIRouter, Depends

from app.database.database import get_session

from app.user.models import User
from app.auth.dependencies import get_current_user
from app.payment.utils import *

from app.payment.models import Transaction

# import aiohttp
import requests


payment_router = APIRouter(tags=["payment"])


@payment_router.post("/api/make_payment")
async def make_payment(
    transaction_id: str,
    amount: float,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    amount = int(amount * 100)

    headers = {
        "content-type": "application/x-www-form-urlencoded",
    }

    data = f"amount={amount}&currency=643&userName=adventuregenerator-api&password=u5**Nk43&returnUrl=google.com&description=my_first_order&language=ru&orderNumber={transaction_id}"

    response = requests.post(
        "https://vtb.rbsuat.com/payment/rest/register.do", headers=headers, data=data
    )

    return response.json()


@payment_router.post("/api/payment_success")
async def on_payment_success(current_user: Annotated[User, Depends(get_current_user)]):
    raise NotImplementedError()
