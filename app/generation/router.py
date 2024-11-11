from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app.adventure.service import (
    get_adventure,
    create_adventure,
)
from app.database.database import get_session
from app.adventure.models import Adventure, AdventurePublic
from app.user.models import User
from app.auth.dependencies import get_current_user

from app.generation.generation_image_service import (
    generate_images_adventure,
    generate_test_images_adventure,
    generate_images_characters,
    generate_test_images_characters,
    generate_images_items,
    generate_test_images_items,
)
from app.generation.generation_text_service import (
    generate_new_adventure_json,
    generate_new_test_adventure_json,
    regenerate_new_adventure_json,
    regenerate_quests_json,
    regenerate_quest_concrete_json,
    regenerate_characters_json,
    regenerate_character_concrete_json,
    regenerate_items_json,
    regenerate_item_concrete_json,
)
from app.generation.text_models import text_generation_model
from app.configs.generation import generation_setting

generation_router = APIRouter(tags=["generation"])


@generation_router.post("/api/adventure", response_model=AdventurePublic)
def generate_adventure(
    num_players: int,
    location_name: str,
    setting: str,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure = create_adventure(current_user.id, session)

    def inner_command(adventure: Adventure):
        adventure = generate_new_adventure_json(
            location_name,
            setting,
            num_players,
            text_generation_model,
            adventure,
            session,
        )
        adventure = generate_images_adventure(adventure, session)
        adventure = generate_images_characters(adventure, session)
        generate_images_items(adventure, session)

    background_tasks.add_task(inner_command, adventure)
    return adventure


@generation_router.post("/api/generate_test", response_model=AdventurePublic)
def generate_test_adventure(
    num_players: int,
    location_name: str,
    setting: str,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure = create_adventure(current_user.id, session)

    def inner_command(adventure: Adventure):
        adventure = generate_new_test_adventure_json(
            location_name,
            setting,
            num_players,
            adventure,
            session,
        )
        adventure = generate_test_images_adventure(adventure, session)
        adventure = generate_test_images_characters(adventure, session)
        generate_test_images_items(adventure, session)

    background_tasks.add_task(inner_command, adventure)
    return adventure


# ============================= QUESTS ========================


@generation_router.put(
    "/api/adventure/{id_adventure}/quests", response_model=AdventurePublic
)
def regenerate_quests(
    id_adventure: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
) -> AdventurePublic:
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure = get_adventure(id_adventure, current_user.id, session)

    background_tasks.add_task(
        regenerate_quests_json, adventure, text_generation_model, session
    )
    return adventure


@generation_router.put(
    "/api/adventure/{id_adventure}/quests/{index_quest}", response_model=AdventurePublic
)
def regenerate_quests_concrete(
    index_quest: int,
    id_adventure: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure = get_adventure(id_adventure, current_user.id, session)
    adventure_info = AdventureInfo.model_validate_json(adventure.content)

    if index_quest < 0 or index_quest >= len(adventure_info.quests):
        return HTTPException(status_code=400, detail="Index out of range")

    background_tasks.add_task(
        regenerate_quest_concrete_json,
        index_quest,
        adventure,
        text_generation_model,
        session,
    )
    return adventure


# ================================ CHARACTERS ===========================


@generation_router.put(
    "/api/adventure/{id_adventure}/characters", response_model=AdventurePublic
)
def regenerate_characters(
    id_adventure: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
) -> AdventurePublic:
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure = get_adventure(id_adventure, current_user.id, session)

    def inner_command(adventure: Adventure):
        adventure = regenerate_characters_json(
            adventure,
            text_generation_model,
            session,
        )
        generate_images_characters(adventure, session)

    background_tasks.add_task(inner_command, adventure)
    return adventure


@generation_router.put(
    "/api/adventure/{id_adventure}/characters/{index_character}",
    response_model=AdventurePublic,
)
def regenerate_characters_concrete(
    id_adventure: int,
    index_character: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure = get_adventure(id_adventure, current_user.id, session)
    adventure_info = AdventureInfo.model_validate_json(adventure.content)

    if index_character < 0 or index_character >= len(adventure_info.characters):
        return HTTPException(status_code=400, detail="Index out of range")

    def inner_command(adventure: Adventure):
        adventure = regenerate_character_concrete_json(
            index_character,
            adventure,
            text_generation_model,
            session,
        )
        generate_images_characters(adventure, session)

    background_tasks.add_task(inner_command, adventure)
    return adventure


# ================================== ITEMS ======================================


@generation_router.put(
    "/api/adventure/{id_adventure}/items", response_model=AdventurePublic
)
def regenerate_items(
    id_adventure: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure = get_adventure(id_adventure, current_user.id, session)

    def inner_command(adventure: Adventure):
        adventure = regenerate_items_json(
            adventure,
            text_generation_model,
            session,
        )
        generate_images_items(adventure, session)

    background_tasks.add_task(inner_command, adventure)
    return adventure


@generation_router.put(
    "/api/adventure/{id_adventure}/items/{index_item}", response_model=AdventurePublic
)
def regenerate_items_concrete(
    index_item: int,
    id_adventure: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure = get_adventure(id_adventure, current_user.id, session)
    adventure_info = AdventureInfo.model_validate_json(adventure.content)

    if index_item < 0 or index_item >= len(adventure_info.items):
        return HTTPException(status_code=400, detail="Index out of range")

    def inner_command(adventure: Adventure):
        adventure = regenerate_item_concrete_json(
            index_item,
            adventure,
            text_generation_model,
            session,
        )
        generate_images_items(adventure, session)

    background_tasks.add_task(inner_command, adventure)
    return adventure
