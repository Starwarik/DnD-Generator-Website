from fastapi import APIRouter, BackgroundTasks, Depends

from sqlmodel import Session
from typing_extensions import Annotated

from app.database.database import get_session
from app.generation.service import generate_adventure_with_models
from ..adventure.models import Adventure
from app.user.models import User
from app.auth.dependencies import get_current_user

generation_router = APIRouter(tags=["generation"])


@generation_router.get("/api/generate")
def generate_adventure(
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    background_tasks.add_task(generate_adventure_with_models, current_user.id, session)
    return "Zaeb'is"
