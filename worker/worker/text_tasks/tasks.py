from worker.database.schemas import AdventureInfo
from worker.database.models import AdventureState
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

from sqlalchemy.orm import Session
from worker.database.database import engine
from worker.database.crud import update_state_content_adventure

from worker.main import celery_app


@celery_app.task(name="main.generate_new_adventure")
def generate_new_adventure(location_name: str, setting: str, num_players: int):
    return generate_new_adventure_json(
        location_name, setting, num_players, text_generation_model
    )


@celery_app.task(name="main.generate_new_test_adventure")
def generate_new_test_adventure(
    id_adventure: int, location_name: str, setting: str, num_players: int
):
    adventure, _ = generate_new_test_adventure_json(location_name, setting, num_players)
    with Session(engine) as session:
        update_state_content_adventure(
            id_adventure, AdventureState.ready, adventure, session
        )
    return id_adventure


@celery_app.task(name="main.regenerate_new_adventure")
def regenerate_new_adventure(
    adventure_info: AdventureInfo,
):
    return regenerate_new_adventure_json(adventure_info, text_generation_model)


@celery_app.task(name="main.regenerate_quests")
def regenerate_quests(
    adventure_info: AdventureInfo,
):
    return regenerate_quests_json(adventure_info, text_generation_model)


@celery_app.task(name="main.regenerate_quest_concrete")
def regenerate_quest_concrete(
    index_quest: int,
    adventure_info: AdventureInfo,
):
    return regenerate_quest_concrete_json(
        index_quest, adventure_info, text_generation_model
    )


@celery_app.task(name="main.regenerate_characters")
def regenerate_characters(
    adventure_info: AdventureInfo,
):
    return regenerate_characters_json(adventure_info, text_generation_model)


@celery_app.task(name="main.regenerate_character_concrete")
def regenerate_character_concrete(
    index_quest: int,
    adventure_info: AdventureInfo,
):
    return regenerate_character_concrete_json(
        index_quest, adventure_info, text_generation_model
    )


@celery_app.task(name="main.regenerate_items")
def regenerate_items(
    adventure_info: AdventureInfo,
):
    return regenerate_items_json(adventure_info, text_generation_model)


@celery_app.task(name="main.regenerate_item_concrete")
def regenerate_item_concrete(
    index_quest: int,
    adventure_info: AdventureInfo,
):
    return regenerate_item_concrete_json(
        index_quest, adventure_info, text_generation_model
    )
