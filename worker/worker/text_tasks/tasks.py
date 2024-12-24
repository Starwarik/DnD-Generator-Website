from worker.database.schemas import AdventureInfo, SpentedTokensCounts
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
from worker.database.crud import update_state_content_adventure, get_adventure

from worker.main import celery_app


@celery_app.task(name="main.generate_new_adventure")
def generate_new_adventure(
    id_adventure: int,
    location_name: str,
    setting: str,
    num_players: int,
):
    adventure, spented_tokens = generate_new_adventure_json(
        location_name, setting, num_players, text_generation_model
    )
    with Session(engine) as session:
        update_state_content_adventure(
            id_adventure, AdventureState.ready, adventure, session
        )
    return (id_adventure, spented_tokens)


@celery_app.task(name="main.generate_new_test_adventure")
def generate_new_test_adventure(
    id_adventure: int,
    location_name: str,
    setting: str,
    num_players: int,
):
    adventure, spented_tokens = generate_new_test_adventure_json(
        location_name, setting, num_players
    )
    with Session(engine) as session:
        update_state_content_adventure(
            id_adventure, AdventureState.ready, adventure, session
        )
    return id_adventure


@celery_app.task(name="main.regenerate_new_adventure")
def regenerate_new_adventure(
    id_adventure: int,
):
    with Session(engine) as session:
        adventure = get_adventure(id_adventure, session)
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    adventure_info, spented_tokens = regenerate_new_adventure_json(
        adventure_info, text_generation_model
    )
    with Session(engine) as session:
        update_state_content_adventure(
            id_adventure, AdventureState.ready, adventure_info, session
        )
    return (id_adventure, spented_tokens)


@celery_app.task(name="main.regenerate_quests")
def regenerate_quests(
    id_adventure: int,
):
    with Session(engine) as session:
        adventure = get_adventure(id_adventure, session)
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    adventure, spented_tokens = regenerate_quests_json(
        adventure_info, text_generation_model
    )
    with Session(engine) as session:
        update_state_content_adventure(
            id_adventure, AdventureState.ready, adventure, session
        )
    return (id_adventure, spented_tokens)


@celery_app.task(name="main.regenerate_quest_concrete")
def regenerate_quest_concrete(
    id_adventure: int,
    index_quest: int,
):
    with Session(engine) as session:
        adventure = get_adventure(id_adventure, session)
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    adventure, spented_tokens = regenerate_quest_concrete_json(
        index_quest, adventure_info, text_generation_model
    )
    with Session(engine) as session:
        update_state_content_adventure(
            id_adventure, AdventureState.ready, adventure, session
        )
    return (id_adventure, spented_tokens)


@celery_app.task(name="main.regenerate_npcs")
def regenerate_npcs(
    id_adventure: int,
):
    with Session(engine) as session:
        adventure = get_adventure(id_adventure, session)
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    adventure, spented_tokens = regenerate_characters_json(
        adventure_info, text_generation_model
    )
    with Session(engine) as session:
        update_state_content_adventure(
            id_adventure, AdventureState.ready, adventure, session
        )
    return (id_adventure, spented_tokens)


@celery_app.task(name="main.regenerate_npc_concrete")
def regenerate_npc_concrete(
    id_adventure: int,
    index_npc: int,
):
    with Session(engine) as session:
        adventure = get_adventure(id_adventure, session)
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    adventure, spented_tokens = regenerate_character_concrete_json(
        index_npc, adventure_info, text_generation_model
    )
    with Session(engine) as session:
        update_state_content_adventure(
            id_adventure, AdventureState.ready, adventure, session
        )
    return (id_adventure, spented_tokens)


@celery_app.task(name="main.regenerate_items")
def regenerate_items(
    id_adventure: int,
):
    with Session(engine) as session:
        adventure = get_adventure(id_adventure, session)
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    adventure, spented_tokens = regenerate_items_json(
        adventure_info, text_generation_model
    )
    with Session(engine) as session:
        update_state_content_adventure(
            id_adventure, AdventureState.ready, adventure, session
        )
    return (id_adventure, spented_tokens)


@celery_app.task(name="main.regenerate_item_concrete")
def regenerate_item_concrete(
    id_adventure: int,
    index_item: int,
):
    with Session(engine) as session:
        adventure = get_adventure(id_adventure, session)
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    adventure, spented_tokens = regenerate_item_concrete_json(
        index_item, adventure_info, text_generation_model
    )
    with Session(engine) as session:
        update_state_content_adventure(
            id_adventure, AdventureState.ready, adventure, session
        )
    return (id_adventure, spented_tokens)
