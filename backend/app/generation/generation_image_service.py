from sqlalchemy.ext.asyncio import AsyncSession

from app.adventure.models import Adventure, AdventureState
from app.adventure.service import update_state_content_adventure
from app.adventure.schemas import AdventureInfo
from app.generation.prompts import *

from app.generation.image_models import image_model

import time

from app.image.service import upload_image


async def _generate_image(
    instruction: str,
    user_id: int,
    session: AsyncSession,
):
    image_container = await image_model.async_generate_image(None, instruction)
    image = await upload_image(image_container, user_id, session)
    return image.id


async def generate_images_adventure(
    adventure: Adventure,
    session: AsyncSession,
    state: AdventureState = AdventureState.image_characters,
) -> Adventure:
    """
    Генерация обложки и карты для всего приключения.

    :param adventure: Приключение, для которого генерируется картинка.
    :param session: для бд
    :param state: состояние, в которое нужно установить приключение, после конца генерации.
    """
    content = AdventureInfo.model_validate_json(adventure.content)
    try:
        if content.map_image_id == -1:
            image_id = await _generate_image(
                map_image_generation.format(
                    location_name=content.location,
                    location_description="\n".join(content.description),
                ),
                adventure.user_id,
                session,
            )
            content.map_image_id = image_id
            time.sleep(10)
    except Exception as e:
        print(e)
    try:
        if content.adventure_image_id == -1:
            image_id = await _generate_image(
                adventure_image_generation.format(
                    location_name=content.location,
                    location_description="\n".join(content.description),
                ),
                adventure.user_id,
                session,
            )
            content.adventure_image_id = image_id
            time.sleep(10)
    except Exception as e:
        print(e)
    return await update_state_content_adventure(adventure.id, state, content, session)


async def generate_test_images_adventure(
    adventure: Adventure,
    session: AsyncSession,
    state: AdventureState = AdventureState.image_characters,
) -> Adventure:
    """
    Тестовая генерация обложек и карты. Вставляются id -42 для изображений.

    :param adventure: Приключение, для которого генерируется картинка.
    :param session: для бд
    :param state: состояние, в которое нужно установить приключение, после конца генерации.
    """
    content = AdventureInfo.model_validate_json(adventure.content)
    content.adventure_image_id = -42
    content.map_image_id = -42
    adventure = await update_state_content_adventure(
        adventure.id, state, content, session
    )
    time.sleep(5)
    return adventure


async def generate_images_characters(
    adventure: Adventure,
    session: AsyncSession,
    state: AdventureState = AdventureState.image_items,
) -> Adventure:
    """
    Генерация картинок персонажей.

    :param adventure: Приключение, для которого генерируется картинка.
    :param session: для бд
    :param state: состояние, в которое нужно установить приключение, после конца генерации.
    """
    content = AdventureInfo.model_validate_json(adventure.content)
    for i in range(len(content.npcs)):
        char = content.npcs[i]
        if char.image_id == -1:
            try:
                image_id = await _generate_image(
                    character_image_generation.format(
                        char_name=char.name, char_description=char.description
                    ),
                    adventure.user_id,
                    session,
                )
                content.npcs[i].image_id = image_id
                time.sleep(10)
            except Exception as e:
                print(e)
    return await update_state_content_adventure(adventure.id, state, content, session)


async def generate_test_images_characters(
    adventure: Adventure,
    session: AsyncSession,
    state: AdventureState = AdventureState.image_items,
) -> Adventure:
    """
    Тестовая генерация картинок персонажей. Вставляются id -42 для изображений персонажей.

    :param adventure: Приключение, для которого генерируется картинка.
    :param session: для бд
    :param state: состояние, в которое нужно установить приключение, после конца генерации.
    """
    content = AdventureInfo.model_validate_json(adventure.content)
    new_items = content.items
    for i, x in enumerate(new_items):
        new_items[i].image_id = -42
    content.items = new_items
    adventure = await update_state_content_adventure(
        adventure.id, state, content, session
    )
    time.sleep(5)
    return adventure


async def generate_images_items(
    adventure: Adventure,
    session: AsyncSession,
    state: AdventureState = AdventureState.ready,
) -> Adventure:
    """
    Генерация картинок предметов.

    :param adventure: Приключение, для которого генерируется картинка.
    :param session: для бд
    :param state: состояние, в которое нужно установить приключение, после конца генерации.
    """
    content = AdventureInfo.model_validate_json(adventure.content)
    for i in range(len(content.items)):
        item = content.items[i]
        if item.image_id == -1:
            try:
                image_id = await _generate_image(
                    item_image_generation.format(
                        item_name=item.name, item_description=item.description
                    ),
                    adventure.user_id,
                    session,
                )
                content.items[i].image_id = image_id
                time.sleep(10)
            except Exception as e:
                print(e)
    return await update_state_content_adventure(adventure.id, state, content, session)


async def generate_test_images_items(
    adventure: Adventure,
    session: AsyncSession,
    state: AdventureState = AdventureState.ready,
) -> Adventure:
    """
    Тестовая генерация картинок предметов. Вставляются id -42 для изображений предме6тов.

    :param adventure: Приключение, для которого генерируется картинка.
    :param session: для бд
    :param state: состояние, в которое нужно установить приключение, после конца генерации.
    """
    content = AdventureInfo.model_validate_json(adventure.content)
    new_characters = content.npcs
    for i, x in enumerate(new_characters):
        new_characters[i].image_id = -42
    content.npcs = new_characters
    adventure = await update_state_content_adventure(
        adventure.id, state, content, session
    )
    time.sleep(5)
    return adventure
