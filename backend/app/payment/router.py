from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse, PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession
import requests
from typing import Any

from app.database.database import get_session
from app.user.models import User
from app.auth.dependencies import get_current_user
from app.payment.config import payment_setting
from app.payment.models import Transaction


payment_router = APIRouter(tags=["payment"])


def create_order(amount: int, order_num: int) -> dict[str, Any]:
    fallback_url = f"https://adventuregenerator.ru/api/payment_success?order_number={order_num}"

    data = {
        "token": payment_setting.alfa_token,
        "amount": amount,
        "currency": "643",
        "orderNumber": str(order_num),
        "returnUrl": fallback_url,
        "failUrl": payment_setting.url_failed_order,
        "description": "my_first_order",
        "language": "ru"
    }

    response = requests.post(
        payment_setting.alfa_base_api + "register.do",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if response.status_code != 200:
        print(f"Ошибка HTTP: {response.status_code}, {response.text}")
        return {"errorCode": "HTTP_ERROR", "errorMessage": response.text}

    try:
        return response.json()
    except ValueError:
        print(f"Ошибка разбора JSON: {response.text}")
        return {"errorCode": "JSON_ERROR", "errorMessage": "Некорректный ответ сервера"}


@payment_router.get("/api/make_payment", response_class=PlainTextResponse)
async def make_payment(
    amount: float,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    try:
        transaction = Transaction(
            user_id=current_user.id,
            amount=amount,
            is_success=False,
        )
        session.add(transaction)
        await session.commit()
        await session.refresh(transaction)

        amount_in_kopecks = int(amount * 100)

        transaction_id = transaction.id - 1
        
        while True:
            transaction_id += 1
            result = create_order(amount_in_kopecks, transaction_id)

            if "errorCode" in result or "formUrl" not in result:
                print("Ошибка при регистрации заказа:", result)
                continue

            existing_transaction = await session.get(Transaction, transaction_id)
            if existing_transaction is not None:
                continue

            break

        transaction.id = transaction_id
        session.add(transaction)
        await session.commit()

        return f'"{result["formUrl"]}"'

    except Exception as e:
        print("Ошибка make_payment:", e)
        raise HTTPException(status_code=500, detail="Ошибка при создании платежа")


@payment_router.get("/api/payment_success")
async def on_payment_success(
    order_number: int,
    orderId: str | None,
    lang: str | None,
    session: AsyncSession = Depends(get_session),
):
    data = {
        "token" : payment_setting.alfa_token,
        "orderId": orderId,
        "language": "ru",
    }

    response = requests.post(
        payment_setting.alfa_base_api + "getOrderStatus.do",
        json=data
    )
    result = response.json()

    if result.get("OrderStatus") not in [1, 2]:
        return RedirectResponse(payment_setting.url_failed_order)

    transaction = await session.get(Transaction, order_number)
    if transaction is None or transaction.is_success:
        return RedirectResponse(payment_setting.url_failed_order)

    user = await session.get(User, transaction.user_id)
    if user is None:
        return RedirectResponse(payment_setting.url_failed_order)

    user.balance += transaction.amount
    transaction.is_success = True

    session.add_all([user, transaction])
    await session.commit()
    await session.flush()

    return RedirectResponse(payment_setting.url_successful_order)
