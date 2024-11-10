from sqlalchemy import RowMapping, select, update
from sqlalchemy.orm import Session
from app.adventure.models import Adventure, AdventurePublic, AdventureState
from app.adventure.schemas import AdventureInfo


def create_adventure(user_id: int, session: Session):
    adventure = Adventure(user_id=user_id, state=AdventureState.generating_text)
    session.add(adventure)
    session.commit()
    session.refresh(adventure)
    return adventure


def get_adventure(
    id: int,
    user_id: int,
    session: Session,
) -> Adventure:
    command = select(Adventure).where(Adventure.id == id, Adventure.user_id == user_id)
    results = session.execute(command).scalars()
    result = results.first()
    if result is None:
        raise Exception()
    return result


def update_state_content_adventure(
    id: int,
    state: AdventureState | None,
    content: AdventureInfo | None,
    session: Session,
) -> Adventure:
    new_values = {}
    if state:
        new_values["state"] = state
    if content:
        new_values["content"] = content.model_dump_json()

    command = (
        update(Adventure)
        .where(Adventure.id == id)
        .values(**new_values)
        .returning(Adventure)
    )
    results = session.execute(command).scalars()
    result = results.one()
    session.commit()
    return result
