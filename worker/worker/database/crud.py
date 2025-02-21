from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from worker.database.models import Adventure, AdventureState, Image, User
from worker.database.schemas import AdventureInfo, ImageContainer, SpentedTokensCounts
from worker.config import generation_setting


def get_user_by_id(id: str, session: Session) -> User | None:
    statement = select(User).where(User.id == id)
    results = session.execute(statement)
    result = results.scalars().first()
    if result is None:
        return None
    return result


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


def change_balance_on_value(id: int, diff_balance: float, session: Session):
    user = get_user_by_id(id, session)
    user.balance += diff_balance
    session.add(user)
    session.commit()


def spend_balance_on_tokens(
    id: int, tokens_count: SpentedTokensCounts, session: Session
):
    diff_balance = (
        tokens_count.gigachat_assistant_token_count
        * generation_setting.gigachat_assistant_token_cost
        + tokens_count.gigachat_prompt_token_count
        * generation_setting.gigachat_prompt_token_cost
        + tokens_count.yandexgpt_assistant_token_count
        * generation_setting.yandexgpt_assistant_token_cost
        + tokens_count.yandexgpt_prompt_token_count
        * generation_setting.yandexgpt_prompt_token_cost
        + tokens_count.image_generated * generation_setting.image_generated_cost
    )
    change_balance_on_value(id, -diff_balance, session)


def delete_adventure(id: int, session: Session):
    adventure = get_adventure(id, session)
    content = AdventureInfo.model_validate(adventure.content)
    images_ids: list[int] = []
    images_ids.append(content.adventure_image_id)
    images_ids.append(content.map_image_id)
    images_ids.extend([item.image_id for item in content.items])
    images_ids.extend([npc.image_id for npc in content.npcs])
    images_ids = list(filter(lambda x: x != -1 and x != -42, images_ids))
    if len(images_ids) != 0:
        command = delete(Image).where(Image.id.in_(images_ids))
        session.execute(command)
        session.commit()
    command = delete(Adventure).where(Adventure.id == id)
    session.execute(command)
    session.commit()
