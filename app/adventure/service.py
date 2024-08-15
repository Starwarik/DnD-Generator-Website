from sqlmodel import Session, select
from app.adventure.models import Adventure, AdventureState
from app.adventure.schemas import AdventureInfo


def create_adventure(user_id: int, session: Session):
    adventure = Adventure(user_id=user_id)
    session.add(adventure)
    session.commit()
    session.refresh(adventure)
    return adventure


def update_state_content_adventure(
    id: int,
    state: AdventureState | None,
    content: AdventureInfo | None,
    session: Session,
):
    command = select(Adventure).where(Adventure.id == id)
    results = session.exec(command)
    result = results.first()
    if result is None:
        raise Exception()
    result.state = state
    result.content = content
    session.add(result)
    session.commit()
    session.refresh(result)
    return result
