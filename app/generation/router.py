from fastapi import APIRouter, BackgroundTasks, Depends

from sqlmodel import Session
from typing_extensions import Annotated

from app.adventure.service import convert_adventure_to_public, create_adventure
from app.database.database import get_session
from app.generation.service import generate_adventure_with_models
from app.adventure.models import AdventurePublic
from app.user.models import User
from app.auth.dependencies import get_current_user

generation_router = APIRouter(tags=["generation"])


@generation_router.get("/api/generate")
def generate_adventure(
    num_players: int,
    location_name: str,
    setting: str,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
) -> AdventurePublic:
    adventure = create_adventure(current_user.id, session)
    background_tasks.add_task(
        generate_adventure_with_models,
        location_name,
        setting,
        num_players,
        current_user.id,
        adventure.id,
        session,
    )
    return convert_adventure_to_public(adventure)
