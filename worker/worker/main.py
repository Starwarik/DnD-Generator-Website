import os
from celery import Celery
from kombu.serialization import register
from worker.text_tasks.schemas import AdventureUpdateWithSpentedResult, AdventureInfo
from worker.text_tasks.generation_text_service import (
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
from worker.text_tasks.text_models import text_generation_model

import worker.pydanticserializer as pydanticserializer

CELERY_BROKER_URL = (os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),)
CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)

register(
    "pydantic",
    pydanticserializer.pydantic_dumps,
    pydanticserializer.pydantic_loads,
    content_type="application/x-pydantic",
    content_encoding="utf-8",
)

celery_app = Celery("celery", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery_app.conf.update(
    broker_connection_retry_on_startup=True,
    task_serializer="pydantic",
    result_serializer="pydantic",
    event_serializer="pydantic",
    accept_content=["application/json", "application/x-pydantic"],
    result_accept_content=["application/json", "application/x-pydantic"],
)


@celery_app.task(name="main.generate_new_adventure")
def generate_new_adventure(
    location_name: str, setting: str, num_players: int
) -> AdventureUpdateWithSpentedResult:
    return generate_new_adventure_json(
        location_name, setting, num_players, text_generation_model
    )


@celery_app.task(name="main.generate_new_test_adventure")
def generate_new_test_adventure(
    location_name: str, setting: str, num_players: int
) -> AdventureUpdateWithSpentedResult:
    return generate_new_test_adventure_json(location_name, setting, num_players)


@celery_app.task(name="main.regenerate_new_adventure")
def regenerate_new_adventure(
    adventure_info: AdventureInfo,
) -> AdventureUpdateWithSpentedResult:
    return regenerate_new_adventure_json(adventure_info, text_generation_model)


@celery_app.task(name="main.regenerate_quests")
def regenerate_quests(
    adventure_info: AdventureInfo,
) -> AdventureUpdateWithSpentedResult:
    return regenerate_quests_json(adventure_info, text_generation_model)


@celery_app.task(name="main.regenerate_quest_concrete")
def regenerate_quest_concrete(
    index_quest: int,
    adventure_info: AdventureInfo,
) -> AdventureUpdateWithSpentedResult:
    return regenerate_quest_concrete_json(
        index_quest, adventure_info, text_generation_model
    )


@celery_app.task(name="main.regenerate_characters")
def regenerate_characters(
    adventure_info: AdventureInfo,
) -> AdventureUpdateWithSpentedResult:
    return regenerate_characters_json(adventure_info, text_generation_model)


@celery_app.task(name="main.regenerate_character_concrete")
def regenerate_character_concrete(
    index_quest: int,
    adventure_info: AdventureInfo,
) -> AdventureUpdateWithSpentedResult:
    return regenerate_character_concrete_json(
        index_quest, adventure_info, text_generation_model
    )


@celery_app.task(name="main.regenerate_items")
def regenerate_items(
    adventure_info: AdventureInfo,
) -> AdventureUpdateWithSpentedResult:
    return regenerate_items_json(adventure_info, text_generation_model)


@celery_app.task(name="main.regenerate_item_concrete")
def regenerate_item_concrete(
    index_quest: int,
    adventure_info: AdventureInfo,
) -> AdventureUpdateWithSpentedResult:
    return regenerate_item_concrete_json(
        index_quest, adventure_info, text_generation_model
    )
