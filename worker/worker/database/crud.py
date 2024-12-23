from sqlalchemy import select, update
from sqlalchemy.orm import Session
from worker.database.models import Adventure, AdventureState, Image
from worker.database.schemas import AdventureInfo, ImageContainer


def get_adventure(
    id: int,
    session: Session,
) -> Adventure:
    command = select(Adventure).where(Adventure.id == id)
    results = session.execute(command)
    result = results.scalars().first()
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
    try:
        command = update(Adventure).where(Adventure.id == id).values(**new_values)
        session.execute(command)
        session.commit()
        return session.get(Adventure, id)

    except Exception as e:
        raise Exception(
            f"""{str(new_values)}
        
        {str(e)}"""
        )


def upload_image(container: ImageContainer, user_id: int, session: Session) -> Image:
    image = Image(
        image=container.content, media_type=container.media_type, user_id=user_id
    )
    session.add(image)
    session.commit()
    session.refresh(image)
    return image
