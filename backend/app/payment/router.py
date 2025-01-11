from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException

from app.database.database import get_session

from app.user.models import User
from app.auth.dependencies import get_current_user
from app.payment.utils import *
from app.payment.config import payment_setting

from app.payment.models import Transaction
from app.user.models import User

from fastapi.responses import RedirectResponse

# import aiohttp
import requests
from typing import Any


payment_router = APIRouter(tags=["payment"])


def create_order(amount: float, order_num: int) -> dict[str, Any]:
    fallback_url = (
        f"https://adventuregenerator.ru/api/payment_success?order_number={order_num}"
    )

    headers = {
        "content-type": "application/x-www-form-urlencoded",
    }

    data = f"amount={amount}&currency=643&userName={payment_setting.vtb_username}&password={payment_setting.vtb_password}&returnUrl={fallback_url}&failUrl={fallback_url}&description=my_first_order&language=ru&orderNumber={order_num}"

    response = requests.post(
        payment_setting.vtb_base_api + "register.do", headers=headers, data=data
    )

    return response.json()


@payment_router.get("/api/make_payment")
async def make_payment(
    amount: float,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    result, transaction_try = "none", "none"
    try:
        transaction = Transaction(
            user_id=current_user.id, amount=amount, is_success=False
        )
        session.add(transaction)
        await session.commit()
        await session.refresh(transaction)

        amount = int(amount * 100)

        is_failed = True
        transaction_id = transaction.id - 1
        while is_failed:
            transaction_id += 1
            result = create_order(amount, transaction_id)
            is_failed = "errorCode" in result

            transaction_try = await session.get(Transaction, transaction_id)

            is_failed = is_failed or (not transaction_try is None)

        transaction.id = transaction_id
        session.add(transaction)
        await session.commit()

        return result["formUrl"]
    except Exception as e:
        print(e, result, transaction_try)
        return HTTPException(404)


@payment_router.get("/api/payment_success")
async def on_payment_success(
    order_number: int,
    orderId: str | None,
    lang: str | None,
    session: AsyncSession = Depends(get_session),
):
    data = {
        "userName": payment_setting.vtb_username,
        "password": payment_setting.vtb_password,
        "orderNumber": order_number,
        "language": "ru",
    }

    response = requests.post(
        payment_setting.vtb_base_api + "getOrderStatusExtended.do", data=data
    )

    result = response.json()

    if result["orderStatus"] == 2 or result["orderStatus"] == 1:
        return result

    transaction = await session.get(Transaction, order_number)

    if transaction is None:
        print("There is no such order")
        return RedirectResponse(payment_setting.url_failed_order)

    if transaction.is_success:
        print("Already proceed")
        return RedirectResponse(payment_setting.url_failed_order)

    user = await session.get(User, transaction.user_id)

    if user is None:
        print("There is no such person")
        return RedirectResponse(payment_setting.url_failed_order)

    user.balance += transaction.amount
    transaction.is_success = True

    session.add(user)
    session.add(transaction)
    await session.commit()
    await session.flush()

    return RedirectResponse(payment_setting.url_successful_order)
