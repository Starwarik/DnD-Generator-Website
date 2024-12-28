from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from app.adventure.schemas import AdventureInfo
from app.adventure.service import (
    get_adventure,
    create_adventure,
)
from app.database.database import get_session
from app.adventure.models import Adventure, AdventurePublic
from app.user.models import User
from app.auth.dependencies import get_current_user

from app.generation.config import generation_setting
from app.generation.celery import celery_app
from celery import chain, signature

generation_router = APIRouter(tags=["generation"])


@generation_router.post("/api/generate", response_model=AdventurePublic)
async def generate_adventure(
    num_players: int,
    location_name: str,
    setting: str,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure: Adventure = await create_adventure(current_user.id, session)

    task = chain(
        signature(
            "main.generate_new_adventure",
            args=(adventure.id, location_name, setting, num_players),
        ),
        signature("main.generate_images_adventure"),
        signature("main.generate_images_npcs"),
        signature("main.generate_images_items"),
        signature("main.finish_generation_and_spent_balance"),
    )
    task()
    return adventure


@generation_router.post("/api/generate_test", response_model=AdventurePublic)
async def generate_test_adventure(
    num_players: int,
    location_name: str,
    setting: str,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    adventure: Adventure = await create_adventure(current_user.id, session)
    task = chain(
        signature(
            "main.generate_new_test_adventure",
            args=(adventure.id, location_name, setting, num_players),
        ),
        signature("main.generate_test_images_adventure"),
        signature("main.generate_test_images_npcs"),
        signature("main.generate_test_images_items"),
    )
    task()
    return adventure


# ============================= QUESTS ========================


@generation_router.get(
    "/api/generate/{id_adventure}/quests", response_model=AdventurePublic
)
async def regenerate_quests(
    id_adventure: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure: Adventure = await get_adventure(id_adventure, current_user.id, session)
    celery_app.send_task(
        "main.regenerate_quests",
        (adventure.id,),
    )
    task = chain(
        signature(
            "main.regenerate_quests",
            args=(adventure.id,),
        ),
        signature("main.finish_generation_and_spent_balance"),
    )
    task()
    return adventure


@generation_router.get(
    "/api/generate/{id_adventure}/quests/{index_quest}", response_model=AdventurePublic
)
async def regenerate_quests_concrete(
    id_adventure: int,
    index_quest: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure: Adventure = await get_adventure(id_adventure, current_user.id, session)
    adventure_info = AdventureInfo.model_validate_json(adventure.content)

    if index_quest < 0 or index_quest >= len(adventure_info.quests):
        return HTTPException(status_code=400, detail="Index out of range")

    task = chain(
        signature(
            "main.regenerate_quest_concrete",
            args=(adventure.id, index_quest),
        ),
        signature("main.finish_generation_and_spent_balance"),
    )
    task()
    return adventure


# ================================ CHARACTERS ===========================


@generation_router.get(
    "/api/generate/{id_adventure}/npcs", response_model=AdventurePublic
)
async def regenerate_npcs(
    id_adventure: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure: Adventure = await get_adventure(id_adventure, current_user.id, session)

    task = chain(
        signature(
            "main.regenerate_npcs",
            args=(adventure.id),
        ),
        signature("main.generate_images_npcs"),
        signature("main.finish_generation_and_spent_balance"),
    )
    task()
    return adventure


@generation_router.get(
    "/api/generate/{id_adventure}/npcs/{index_npc}",
    response_model=AdventurePublic,
)
async def regenerate_characters_concrete(
    id_adventure: int,
    index_npc: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure: Adventure = await get_adventure(id_adventure, current_user.id, session)
    adventure_info = AdventureInfo.model_validate_json(adventure.content)

    if index_npc < 0 or index_npc >= len(adventure_info.npcs):
        return HTTPException(status_code=400, detail="Index out of range")

    task = chain(
        signature(
            "main.regenerate_npc_concrete",
            args=(adventure.id, index_npc),
        ),
        signature("main.generate_images_npcs"),
        signature("main.finish_generation_and_spent_balance"),
    )
    task()
    return adventure


# ================================== ITEMS ======================================


@generation_router.get(
    "/api/generate/{id_adventure}/items", response_model=AdventurePublic
)
async def regenerate_items(
    id_adventure: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure: Adventure = await get_adventure(id_adventure, current_user.id, session)

    task = chain(
        signature(
            "main.regenerate_items",
            args=(adventure.id,),
        ),
        signature("main.generate_images_items"),
        signature("main.finish_generation_and_spent_balance"),
    )
    task()
    return adventure


@generation_router.get(
    "/api/generate/{id_adventure}/items/{index_item}", response_model=AdventurePublic
)
async def regenerate_items_concrete(
    id_adventure: int,
    index_item: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure: Adventure = await get_adventure(id_adventure, current_user.id, session)
    adventure_info = AdventureInfo.model_validate_json(adventure.content)

    if index_item < 0 or index_item >= len(adventure_info.items):
        return HTTPException(status_code=400, detail="Index out of range")

    task = chain(
        signature(
            "main.regenerate_item_concrete",
            args=(adventure.id, index_item),
        ),
        signature("main.generate_images_items"),
        signature("main.finish_generation_and_spent_balance"),
    )
    task()
    return adventure
