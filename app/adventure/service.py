from sqlmodel import Session, select
from app.adventure.models import Adventure, AdventurePublic, AdventureState
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
    if state:
        result.state = state
    if content:
        result.content = content.model_dump_json()
    else:
        result.content = None
    session.add(result)
    session.commit()
    session.refresh(result)
    return result


def convert_adventure_to_public(adventure: Adventure) -> AdventurePublic:
    adventure_transcript = adventure.model_dump()
    if not (adventure_transcript["content"] is None):
        adventure_transcript["content"] = AdventureInfo.model_validate_json(
            adventure_transcript["content"]
        )
    return AdventurePublic.model_validate(adventure_transcript)
