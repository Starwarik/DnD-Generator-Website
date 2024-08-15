from fastapi import APIRouter, Depends

from sqlmodel import Session, select
from typing_extensions import Annotated

from app.database.database import get_session
from app.adventure.models import Adventure
from app.user.models import User
from app.auth.dependencies import get_current_user

adventure_router = APIRouter(tags=["adventure"])


@adventure_router.get("/api/adventures")
def get_user_adventure(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    command = select(Adventure).where(Adventure.user_id == current_user.id)
    results = session.exec(command)
    return results.all()


@adventure_router.get("/api/adventures/{adventure_id}")
def get_adventure(
    current_user: Annotated[User, Depends(get_current_user)],
    adventure_id: int,
    session: Session = Depends(get_session),
):
    command = (
        select(Adventure)
        .where(Adventure.user_id == current_user.id)
        .where(Adventure.id == adventure_id)
    )
    results = session.exec(command)
    return results.first()
