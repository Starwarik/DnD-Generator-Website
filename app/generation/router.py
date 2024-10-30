from fastapi import APIRouter, BackgroundTasks, Depends

from sqlmodel import Session
from typing_extensions import Annotated

from app.adventure.service import convert_adventure_to_public, get_adventure
from app.database.database import get_session
from app.generation.service import *
from app.adventure.models import AdventurePublic
from app.user.models import User
from app.auth.dependencies import get_current_user

generation_router = APIRouter(tags=["generation"])


"""
@generation_router.get("/api/generate_test")
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
        generate_adventure_test,
        location_name,
        setting,
        num_players,
        adventure.id,
        background_tasks,
        session,
    )
    return convert_adventure_to_public(adventure)
"""


@generation_router.post("/api/adventure")
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
        background_tasks,
        session,
    )
    return convert_adventure_to_public(adventure)


# ============================= QUESTS ========================


@generation_router.put("/api/adventure/{id_adventure}/quests")
def regenerate_quests(
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


@generation_router.put("/api/adventure/{id_adventure}/quests/{index_quest}")
def regenerate_quests_concrete(
    index_quest: int,
    id_adventure: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
) -> AdventurePublic:
    adventure = get_adventure(id_adventure, current_user.id, session)
    background_tasks.add_task(
        regenerate_quest_concrete_with_models,
        adventure,
        index_quest,
        session,
    )
    return convert_adventure_to_public(adventure)


# ================================ CHARACTERS ===========================


@generation_router.put("/api/adventure/{id_adventure}/characters")
def regenerate_characters_concrete(
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


@generation_router.put("/api/adventure/{id_adventure}/characters/{index_character}")
def regenerate_characters(
    id_adventure: int,
    index_character: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
) -> AdventurePublic:
    raise NotImplementedError()


# ================================== ITEMS ======================================


@generation_router.put("/api/adventure/{id_adventure}/items")
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


@generation_router.put("/api/adventure/{id_adventure}/items/{index_item}")
def regenerate_items_concrete(
    index_quest: int,
    id_adventure: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
) -> AdventurePublic:
    adventure = get_adventure(id_adventure, current_user.id, session)
    background_tasks.add_task(
        regenerate_items_concrete_with_models,
        adventure,
        index_quest,
        session,
    )
    return convert_adventure_to_public(adventure)


# ======================================================================================


@generation_router.get("/api/refresh_images")
def refresh_images(
    id_adventure: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
) -> AdventurePublic:
    adventure = get_adventure(id_adventure, current_user.id, session)
    background_tasks.add_task(
        generate_all_images,
        adventure,
        session,
    )
    return convert_adventure_to_public(adventure)
