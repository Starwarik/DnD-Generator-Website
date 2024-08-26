from fastapi import APIRouter, BackgroundTasks, Depends

from sqlmodel import Session
from typing_extensions import Annotated

from app.adventure.schemas import AdventureInfo
from app.adventure.service import convert_adventure_to_public, create_adventure, get_adventure, update_state_content_adventure
from app.database.database import get_session
from app.generation.service import *
from app.adventure.models import AdventurePublic, AdventureState
from app.generation.service import _generate_image
from app.generation.service import __generate_image
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
        adventure.id,
        session,
    )
    return convert_adventure_to_public(adventure)

@generation_router.get("/api/generate_quest")
def regenerate_quest(
    id_adventure: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
) -> AdventurePublic:
    adventure = get_adventure(id_adventure, current_user.id, session)
    background_tasks.add_task(
        regenerate_quest_with_models,
        adventure,
        session,
    )
    return convert_adventure_to_public(adventure)

@generation_router.get("/api/generate_characters")
def regenerate_quest(
    id_adventure: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
) -> AdventurePublic:
    adventure = get_adventure(id_adventure, current_user.id, session)
    background_tasks.add_task(
        regenerate_character_with_models,
        adventure,
        session,
    )
    return convert_adventure_to_public(adventure)

@generation_router.get("/api/generate_items")
def regenerate_items(
    id_adventure: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
) -> AdventurePublic:
    adventure = get_adventure(id_adventure, current_user.id, session)
    background_tasks.add_task(
        regenerate_items_with_models,
        adventure,
        session,
    )
    return convert_adventure_to_public(adventure)

@generation_router.get("/api/change_annotation")
def change_annotation(
    id_adventure: int,
    new_description: str,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
) -> AdventurePublic:
    adventure = get_adventure(id_adventure, current_user.id, session)
    content = AdventureInfo.model_validate_json(adventure.content)
    content.description = new_description
    update_state_content_adventure(
        adventure.id,
        AdventureState.ready,
        content,
        session
    )
    return convert_adventure_to_public(adventure)

@generation_router.get("/api/generate_image")
def generate_image(
    prompt: str,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    return __generate_image(prompt, current_user.id, session)