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


if app_setting.is_test:

    @user_router.get("/api/get_users")
    async def get_all_users(session: AsyncSession = Depends(get_session)):
        statement = select(User)
        results = await session.execute(statement)
        result = results.scalars().all()
        return result

    @user_router.post("/api/infinite_money/{user_id}")
    async def get_infinite_money(
        user_id: int, session: AsyncSession = Depends(get_session)
    ):
        statement = (
            update(User)
            .where(User.id == user_id)
            .values(balance=99999999999999999999999999)
        )
        await session.execute(statement)
        await session.commit()
=======
>>>>>>> main
