from worker.database.models import Adventure, AdventureState
from worker.database.crud import update_state_content_adventure, get_adventure
from worker.database.schemas import AdventureInfo
from worker.database.database import engine

from worker.image_tasks.prompts import *

from worker.main import celery_app

from sqlalchemy.orm import Session

import time

# ================= IMAGE ============================


def _generate_image(
    instruction: str,
    user_id: int,
):
    image_container = image_model.async_generate_image(None, instruction)
    image = upload_image(image_container, user_id, session)
    return image.id


def generate_images_adventure(
    adventure: Adventure,
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
            image_id = _generate_image(
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
    return update_state_content_adventure(adventure.id, state, content, session)


def generate_images_characters(
    adventure: Adventure,
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


def generate_images_items(
    adventure: Adventure,
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


# ================= TEST IMAGE =======================


@celery_app.task(name="main.generate_test_images_adventure")
def generate_test_images_adventure(
    id_adventure: int,
    state: AdventureState = AdventureState.image_characters,
) -> int:
    """
    Тестовая генерация обложек и карты. Вставляются id -42 для изображений.

    :param adventure: Приключение, для которого генерируется картинка.
    :param session: для бд
    :param state: состояние, в которое нужно установить приключение, после конца генерации.
    """
    print("ID:", id_adventure)
    with Session(engine) as session:
        adventure = get_adventure(id_adventure, session)
    content = AdventureInfo.model_validate_json(adventure.content)
    content.adventure_image_id = -42
    content.map_image_id = -42
    with Session(engine) as session:
        adventure = update_state_content_adventure(
            adventure.id, state, content, session
        )
    time.sleep(3)
    return id_adventure


@celery_app.task(name="main.generate_test_images_characters")
def generate_test_images_characters(
    id_adventure: int,
    state: AdventureState = AdventureState.image_items,
) -> int:
    """
    Тестовая генерация картинок персонажей. Вставляются id -42 для изображений персонажей.

    :param adventure: Приключение, для которого генерируется картинка.
    :param session: для бд
    :param state: состояние, в которое нужно установить приключение, после конца генерации.
    """
    with Session(engine) as session:
        adventure = get_adventure(id_adventure, session)
    content = AdventureInfo.model_validate_json(adventure.content)
    new_items = content.items
    for i in range(len(new_items)):
        new_items[i].image_id = -42
    content.items = new_items
    time.sleep(3)
    with Session(engine) as session:
        adventure = update_state_content_adventure(
            adventure.id, state, content, session
        )
    return id_adventure


@celery_app.task(name="main.generate_test_images_items")
def generate_test_images_items(
    id_adventure: int,
    state: AdventureState = AdventureState.ready,
) -> int:
    """
    Тестовая генерация картинок предметов. Вставляются id -42 для изображений предме6тов.

    :param adventure: Приключение, для которого генерируется картинка.
    :param session: для бд
    :param state: состояние, в которое нужно установить приключение, после конца генерации.
    """
    with Session(engine) as session:
        adventure = get_adventure(id_adventure, session)
    content = AdventureInfo.model_validate_json(adventure.content)
    new_characters = content.npcs
    for i in range(len(new_characters)):
        new_characters[i].image_id = -42
    content.npcs = new_characters
    time.sleep(3)
    with Session(engine) as session:
        adventure = update_state_content_adventure(
            adventure.id, state, content, session
        )
    return id_adventure
