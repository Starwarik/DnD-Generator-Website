from typing_extensions import Annotated
from fastapi import APIRouter, Depends

from app.database.database import get_session

from app.user.models import User
from app.auth.dependencies import get_current_user
from app.payment.utils import *

from app.payment.models import Transaction

import aiohttp

payment_router = APIRouter(tags=["payment"])


@payment_router.post("/api/make_payment")
async def make_payment(
    amount: float,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    transaction = Transaction(user_id=current_user.id, amount=amount, is_success=False)
    session.add(transaction)
    await session.commit()
    await session.refresh(transaction)

    amount = int(amount * 100)

    async with aiohttp.ClientSession() as http_session:
        data = f"amount={amount}&currency=643&userName=adventuregenerator-api&password=u5**Nk43&returnUrl=google.com&description=my_first_order&language=ru&orderNumber={transaction.id}"
        async with http_session.post(
            "https://vtb.rbsuat.com/payment/rest/register.do", data=data
        ) as response:
            html = await response.text()
    return html


@payment_router.post("/api/payment_success")
async def on_payment_success(current_user: Annotated[User, Depends(get_current_user)]):
    raise NotImplementedError()
