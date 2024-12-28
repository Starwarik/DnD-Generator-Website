from typing_extensions import Annotated
from fastapi import APIRouter, Depends

from app.database.database import get_session

from app.user.models import User
from app.auth.dependencies import get_current_user
from app.payment.utils import *

from app.payment.models import Transaction, User

# import aiohttp
import requests


payment_router = APIRouter(tags=["payment"])


@payment_router.get("/api/make_payment")
async def make_payment(
    transaction_id: str,
    amount: float,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    transaction = Transaction(user_id=current_user.id, amount=amount, is_success=False)
    session.add(transaction)
    await session.commit()
    await session.refresh(transaction)

    amount = int(amount * 100)
    username_vtb = "adventuregenerator-api"
    password_vtb = "u5**Nk43"
    success_url = "http://127.0.0.1:8004/api/payment_success?order_id={transaction_id}"

    headers = {
        "content-type": "application/x-www-form-urlencoded",
    }

    data = f"amount={amount}&currency=643&userName={username_vtb}&password={password_vtb}&returnUrl={success_url}&description=my_first_order&language=ru&orderNumber={transaction_id}"

    response = requests.post(
        "https://vtb.rbsuat.com/payment/rest/register.do", headers=headers, data=data
    )

    return response.json()["formUrl"]


@payment_router.get("/api/payment_success")
async def on_payment_success(
    order_id: int, session: AsyncSession = Depends(get_session)
):
    data = {
        "userName": "adventuregenerator-api",
        "password": "u5**Nk43",
        "orderId": order_id,
        "language": "ru",
    }

    response = requests.post(
        "https://vtb.rbsuat.com/payment/rest/getOrderStatusExtended.do", data=data
    )

    if response.json()["errorCode"] != 0:
        raise Exception("Not sucessful")

    transaction = await session.get(Transaction, order_id)

    if transaction is None:
        raise Exception("There is no such order")

    if transaction.is_success:
        raise Exception("Already proceed")

    user = await session.get(User, transaction.user_id)

    if user is None:
        raise Exception("There is no such person")

    user.balance += transaction.amount
    transaction.is_success = True

    session.add(user)
    session.add(transaction)
    await session.commit()
    await session.flush()
