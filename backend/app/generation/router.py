from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from app.adventure.schemas import AdventureInfo
from app.adventure.service import (
    get_adventure,
    create_adventure,
    update_state_content_adventure,
)
from app.database.database import get_session
from app.adventure.models import Adventure, AdventurePublic, AdventureState
from app.user.models import User
from app.auth.dependencies import get_current_user

from app.generation.config import generation_setting
from app.generation.schemas import SpentedTokensCounts
from app.generation.celery import celery_app
from celery import chain, signature
from app.database.crud import spend_balance_on_tokens

generation_router = APIRouter(tags=["generation"])


@generation_router.post("/api/adventure", response_model=AdventurePublic)
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
    )
    task()

    # await spend_balance_on_tokens(current_user.id, spented_tokens_counts, session)

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
        signature("main.generate_test_images_characters"),
        signature("main.generate_test_images_items"),
    )
    task()
    return adventure


# ============================= QUESTS ========================


@generation_router.put(
    "/api/adventure/{id_adventure}/quests", response_model=AdventurePublic
)
async def regenerate_quests(
    id_adventure: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    async def inner_command(adventure: Adventure):
        result = celery_app.send_task(
            "main.regenerate_quests",
            (AdventureInfo.model_validate_json(adventure.content),),
        ).get()
        adventure_info = AdventureInfo.model_validate(result["new_adventure_info"])
        spented_tokens_counts = SpentedTokensCounts.model_validate(
            result["spented_tokens_counts"]
        )
        adventure = await update_state_content_adventure(
            adventure.id, AdventureState.image_adventure, adventure_info, session
        )
        await spend_balance_on_tokens(current_user.id, spented_tokens_counts, session)

    adventure: Adventure = await get_adventure(id_adventure, current_user.id, session)

    background_tasks.add_task(inner_command, adventure)
    return adventure


@generation_router.put(
    "/api/adventure/{id_adventure}/quests/{index_quest}", response_model=AdventurePublic
)
async def regenerate_quests_concrete(
    index_quest: int,
    id_adventure: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    async def inner_command(adventure: Adventure, index_quest: int):
        result = celery_app.send_task(
            "main.regenerate_quest_concrete",
            (index_quest, AdventureInfo.model_validate_json(adventure.content)),
        ).get()
        adventure_info = AdventureInfo.model_validate(result["new_adventure_info"])
        spented_tokens_counts = SpentedTokensCounts.model_validate(
            result["spented_tokens_counts"]
        )
        adventure = await update_state_content_adventure(
            adventure.id, AdventureState.image_adventure, adventure_info, session
        )
        await spend_balance_on_tokens(current_user.id, spented_tokens_counts, session)

    adventure: Adventure = await get_adventure(id_adventure, current_user.id, session)
    adventure_info = AdventureInfo.model_validate_json(adventure.content)

    if index_quest < 0 or index_quest >= len(adventure_info.quests):
        return HTTPException(status_code=400, detail="Index out of range")

    background_tasks.add_task(inner_command, adventure, index_quest)
    return adventure


# ================================ CHARACTERS ===========================


@generation_router.put(
    "/api/adventure/{id_adventure}/characters", response_model=AdventurePublic
)
async def regenerate_characters(
    id_adventure: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure: Adventure = await get_adventure(id_adventure, current_user.id, session)

    async def inner_command(adventure: Adventure):
        result = celery_app.send_task(
            "main.regenerate_characters",
            (AdventureInfo.model_validate_json(adventure.content),),
        ).get()
        adventure_info = AdventureInfo.model_validate(result["new_adventure_info"])
        spented_tokens_counts = SpentedTokensCounts.model_validate(
            result["spented_tokens_counts"]
        )
        adventure = await update_state_content_adventure(
            adventure.id, AdventureState.image_adventure, adventure_info, session
        )
        await generate_images_characters(adventure, session)
        await spend_balance_on_tokens(current_user.id, spented_tokens_counts, session)

    background_tasks.add_task(inner_command, adventure)
    return adventure


@generation_router.put(
    "/api/adventure/{id_adventure}/characters/{index_character}",
    response_model=AdventurePublic,
)
async def regenerate_characters_concrete(
    id_adventure: int,
    index_character: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure: Adventure = await get_adventure(id_adventure, current_user.id, session)
    adventure_info = AdventureInfo.model_validate_json(adventure.content)

    if index_character < 0 or index_character >= len(adventure_info.npcs):
        return HTTPException(status_code=400, detail="Index out of range")

    async def inner_command(adventure: Adventure):
        result = celery_app.send_task(
            "main.regenerate_character_concrete",
            (index_character, AdventureInfo.model_validate_json(adventure.content)),
        ).get()
        adventure_info = AdventureInfo.model_validate(result["new_adventure_info"])
        spented_tokens_counts = SpentedTokensCounts.model_validate(
            result["spented_tokens_counts"]
        )
        adventure = await update_state_content_adventure(
            adventure.id, AdventureState.image_adventure, adventure_info, session
        )
        await generate_images_characters(adventure, session)
        await spend_balance_on_tokens(current_user.id, spented_tokens_counts, session)

    background_tasks.add_task(inner_command, adventure)
    return adventure


# ================================== ITEMS ======================================


@generation_router.put(
    "/api/adventure/{id_adventure}/items", response_model=AdventurePublic
)
async def regenerate_items(
    id_adventure: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure: Adventure = await get_adventure(id_adventure, current_user.id, session)

    async def inner_command(adventure: Adventure):
        result = celery_app.send_task(
            "main.regenerate_items",
            (AdventureInfo.model_validate_json(adventure.content),),
        ).get()
        adventure_info = AdventureInfo.model_validate(result["new_adventure_info"])
        spented_tokens_counts = SpentedTokensCounts.model_validate(
            result["spented_tokens_counts"]
        )
        adventure = await update_state_content_adventure(
            adventure.id, AdventureState.image_adventure, adventure_info, session
        )
        await generate_images_items(adventure, session)
        await spend_balance_on_tokens(current_user.id, spented_tokens_counts, session)

    background_tasks.add_task(inner_command, adventure)
    return adventure


@generation_router.put(
    "/api/adventure/{id_adventure}/items/{index_item}", response_model=AdventurePublic
)
async def regenerate_items_concrete(
    index_item: int,
    id_adventure: int,
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    if current_user.balance < generation_setting.min_balance_to_generate:
        raise HTTPException(402, detail="Не достаточно денег на балансе для генерации.")

    adventure: Adventure = await get_adventure(id_adventure, current_user.id, session)
    adventure_info = AdventureInfo.model_validate_json(adventure.content)

    if index_item < 0 or index_item >= len(adventure_info.items):
        return HTTPException(status_code=400, detail="Index out of range")

    async def inner_command(adventure: Adventure):
        result = celery_app.send_task(
            "main.regenerate_item_concrete",
            (index_item, AdventureInfo.model_validate_json(adventure.content)),
        ).get()
        adventure_info = AdventureInfo.model_validate(result["new_adventure_info"])
        spented_tokens_counts = SpentedTokensCounts.model_validate(
            result["spented_tokens_counts"]
        )
        adventure = await update_state_content_adventure(
            adventure.id, AdventureState.image_adventure, adventure_info, session
        )
        await generate_images_items(adventure, session)
        await spend_balance_on_tokens(current_user.id, spented_tokens_counts, session)

    background_tasks.add_task(inner_command, adventure)
    return adventure
