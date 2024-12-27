from worker.database.schemas import SpentedTokensCounts
from worker.database.models import AdventureState
from worker.main import celery_app
from worker.database.crud import (
    spend_balance_on_tokens,
    get_adventure,
    update_state_content_adventure,
)
from worker.database.database import engine

from sqlalchemy.orm import Session


@celery_app.task(name="main.finish_generation_and_spent_balance")
def generate_images_npcs(
    id_adventure_and_spented_tokens: tuple[int, SpentedTokensCounts]
):
    id_adventure, spented_tokens = id_adventure_and_spented_tokens
    with Session(engine) as session:
        adventure = get_adventure(id_adventure, session)
        spend_balance_on_tokens(adventure.user_id, spented_tokens, session)
        update_state_content_adventure(
            id_adventure, AdventureState.ready, None, session
        )
