from typing import Any
from fastapi import BackgroundTasks
from sqlmodel import Session

from app.adventure.models import Adventure, AdventureState
from app.adventure.service import create_adventure, update_state_content_adventure
from app.adventure.schemas import AdventureInfo, Character, Item, Quest
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from app.generation.generation_service import generate_new_adventure
from app.generation.prompts import *

from app.generation.client_image import image_model
from app.generation.client_text import text_generation_model

import json
import time

from app.image.service import upload_image

MessageType = HumanMessage | SystemMessage | AIMessage


def _generate_image(
    instruction: str,
    user_id: int,
    session: Session,
):
    image_container = image_model.generate_image(None, instruction)
    image = upload_image(image_container, user_id, session)
    return image.id


def generate_images_adventure(
    adventure: Adventure, session: Session, state: AdventureState = AdventureState.ready
):
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
        if content.adventure_image_id == -1:
            image_id = _generate_image(
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
    update_state_content_adventure(adventure.id, state, content, session)


def generate_images_characters(
    adventure: Adventure, session: Session, state: AdventureState = AdventureState.ready
):
    content = AdventureInfo.model_validate_json(adventure.content)
    for i in range(len(content.characters)):
        char = content.characters[i]
        if char.image_id == -1:
            try:
                image_id = _generate_image(
                    character_image_generation.format(
                        char_name=char.name, char_description=char.description
                    ),
                    adventure.user_id,
                    session,
                )
                content.characters[i].image_id = image_id
                time.sleep(10)
            except Exception as e:
                print(e)
    update_state_content_adventure(adventure.id, state, content, session)


def generate_images_items(
    adventure: Adventure, session: Session, state: AdventureState = AdventureState.ready
):
    content = AdventureInfo.model_validate_json(adventure.content)
    for i in range(len(content.items)):
        item = content.items[i]
        if item.image_id == -1:
            try:
                image_id = _generate_image(
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
    update_state_content_adventure(adventure.id, state, content, session)


def _make_chat_logs(adventure_info: AdventureInfo):
    extra_info = {
        "nameLocation": adventure_info.location,
        "nameSetting": adventure_info.setting,
        "playerNum": str(adventure_info.playerNum),
        "playerNumXthree": str(adventure_info.playerNum * 3),
    }
    messages = [
        generate_prompt.format(**extra_info),
        json.dumps(
            {
                "location": {
                    "name": adventure_info.location,
                    "setting": adventure_info.setting,
                    "description": adventure_info.description,
                }
            }
        ),
        items_prompt.format(**extra_info),
        json.dumps({"item": [x.model_dump() for x in adventure_info.items]}),
        characters_prompt.format(**extra_info),
        json.dumps({"player": [x.model_dump() for x in adventure_info.characters]}),
        quest_prompt.format(**extra_info),
        json.dumps({"quests": [x.model_dump() for x in adventure_info.quests]}),
    ]
    return [
        HumanMessage(x) if i % 2 == 0 else AIMessage(x) for i, x in enumerate(messages)
    ]


def parse_json_garbage(s):
    s = s[next(idx for idx, c in enumerate(s) if c in "{[") :]
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        return json.loads(s[: e.pos])


def _generate_iterative_chat(
    instructions: list[str],
    extra_info: dict[str, str],
    previous_chat: list[MessageType] = [],
) -> tuple[list[dict], list[MessageType]]:
    messages = previous_chat
    out = []
    for instruction in instructions:
        instruction = instruction.format(**extra_info)
        messages.append(HumanMessage(instruction))
        generated_text = text_generation_model.generate_text(messages)
        print("GENERATED TEXT: ", generated_text)
        try:
            out.append(parse_json_garbage(generated_text))
            messages.append(AIMessage(generated_text))
            time.sleep(10)
        except Exception:
            print(generated_text)
            return out, messages
    return out, messages


def generate_all_images(adventure: Adventure, session: Session):
    generate_images_adventure(adventure, session, state=AdventureState.image_items)
    time.sleep(20)
    generate_images_items(adventure, session, state=AdventureState.image_characters)
    time.sleep(20)
    generate_images_characters(adventure, session, state=AdventureState.ready)


def generate_with_tries(
    func_success, user_messages, num_players, extra_info: dict[str, Any]
):
    extra_info.update(
        {"playerNum": str(num_players), "playerNumXthree": str(num_players * 3)}
    )
    out, messages = [], []
    for tries in range(5):
        out_try, messages = _generate_iterative_chat(
            user_messages[len(out) :], extra_info, messages
        )
        print([(type(x), x.content) for x in messages])
        out += out_try
        if len(out) == len(user_messages):
            func_success(out)
            return
        else:
            messages.pop()
            print(len(messages))
            print(tries, "try of generation")
    print(messages)
    raise Exception()


def generate_adventure_with_models(
    location_name: str,
    setting: str,
    num_players: int,
    adventure_id: int,
    background_tasks: BackgroundTasks,
    session: Session,
):
    adventure_info = generate_new_adventure(
        location_name, setting, num_players, text_generation_model
    )
    adventure = update_state_content_adventure(
        adventure_id, AdventureState.image_adventure, adventure_info, session
    )
    background_tasks.add_task(
        generate_all_images,
        adventure,
        session,
    )


def generate_adventure_test(
    location_name: str,
    setting: str,
    num_players: int,
    adventure_id: int,
    background_tasks: BackgroundTasks,
    session: Session,
):
    time.sleep(5)
    dummy_adventure = {
        "name": "Test adventure",
        "annotation": "",
        "description": "Test location description",
        "location": location_name,
        "setting": setting,
        "playerNum": num_players,
        "characters": [
            {
                "name": "Test character 1",
                "description": "Test description of character 1",
            },
            {
                "name": "Test character 2",
                "description": "Test description of character 2",
            },
            {
                "name": "Test character 3",
                "description": "Test description of character 3",
            },
        ],
        "items": [
            {"name": "Test item 1", "description": "Test description of item 1"},
            {"name": "Test item 2", "description": "Test description of item 2"},
            {"name": "Test item 3", "description": "Test description of item 3"},
        ],
        "quests": [
            {
                "name": "Test quest 1",
                "description": "Test description of quest 1",
                "goal": "Test goal of quest 1",
                "name_character": "Test character 3",
                "name_items": [],
            },
            {
                "name": "Test quest 2",
                "description": "Test description of quest 2",
                "goal": "Test goal of quest 2",
                "name_character": "Test character 1",
                "name_items": ["Test item 1", "Test item 3"],
            },
            {
                "name": "Test quest 3",
                "description": "Test description of quest 3",
                "goal": "Test goal of quest 3",
                "name_character": "Test character 2",
                "name_items": ["Test item 2"],
            },
        ],
    }
    adventure_info = AdventureInfo.model_validate(dummy_adventure)
    update_state_content_adventure(
        adventure_id, AdventureState.image_adventure, adventure_info, session
    )
    time.sleep(5)
    adventure_info.adventure_image_id = -42
    adventure_info.map_image_id = -42
    update_state_content_adventure(
        adventure_id, AdventureState.image_items, adventure_info, session
    )
    time.sleep(5)
    new_items = adventure_info.items
    for i, x in enumerate(new_items):
        new_items[i].image_id = -42
    adventure_info.items = new_items
    update_state_content_adventure(
        adventure_id, AdventureState.image_characters, adventure_info, session
    )
    time.sleep(5)
    new_characters = adventure_info.characters
    for i, x in enumerate(new_characters):
        new_characters[i].image_id = -42
    adventure_info.characters = new_characters
    update_state_content_adventure(
        adventure_id, AdventureState.ready, adventure_info, session
    )


def regenerate_quest_with_models(
    adventure: Adventure,
    session: Session,
):
    content = AdventureInfo.model_validate_json(adventure.content)
    extra_info = {
        "playerNum": str(content.playerNum),
        "playerNumXthree": str(content.playerNum * 3),
    }
    messages = _make_chat_logs(content)
    for tries in range(5):
        out_try, _ = _generate_iterative_chat(
            [quest_regeneration_prompt], extra_info, messages
        )
        if len(out_try) == 1:
            print(out_try)
            content.quests = [
                Quest(
                    name=x["name"],
                    description=x["description"],
                    goal=x["goal"],
                    name_character=x["name_character"],
                    name_items=x["name_items"],
                )
                for x in out_try[0]["quests"]
            ]
            adventure = update_state_content_adventure(
                adventure.id, AdventureState.ready, content, session
            )
        else:
            print(tries, "try of generation")
    print(messages)
    raise Exception()


def regenerate_quest_concrete_with_models(
    adventure: Adventure,
    index_quest: int,
    session: Session,
):
    content = AdventureInfo.model_validate_json(adventure.content)
    extra_info = {
        "nameLocation": content.location,
        "nameSetting": content.setting,
        "playerNum": str(content.playerNum),
        "playerNumXthree": str(content.playerNum * 3),
    }
    messages = _make_chat_logs(content)
    for tries in range(5):
        out_try, _ = _generate_iterative_chat(
            [quest_regeneration_concrete_prompt], extra_info, messages
        )
        if len(out_try) == 1:
            print(out_try)
            content.quests[index_quest] = Quest(
                name=out_try[0]["name"],
                description=out_try[0]["description"],
                goal=out_try[0]["goal"],
                name_character=out_try[0]["name_character"],
                name_items=out_try[0]["name_items"],
            )
            adventure = update_state_content_adventure(
                adventure.id, AdventureState.ready, content, session
            )
        else:
            print(tries, "try of generation")
    print(messages)
    raise Exception()


def regenerate_character_concrete_with_models(
    adventure: Adventure,
    index_character: int,
    session: Session,
):
    content = AdventureInfo.model_validate_json(adventure.content)
    extra_info = {
        "nameLocation": content.location,
        "nameSetting": content.setting,
        "playerNum": str(content.playerNum),
        "playerNumXthree": str(content.playerNum * 3),
    }
    messages = _make_chat_logs(content)
    for tries in range(5):
        out_try, _ = _generate_iterative_chat(
            [characters_regeneration_concrete_prompt], extra_info, messages
        )
        if len(out_try) == 1:
            print(out)
            content.characters[index_character] = Character(
                name=out_try[0]["name"], description=out_try[0]["description"]
            )
            adventure = update_state_content_adventure(
                adventure.id, AdventureState.image_characters, content, session
            )
            generate_images_characters(adventure, session, state=AdventureState.ready)
        else:
            print(tries, "try of generation")
    print(messages)
    raise Exception()


def regenerate_character_with_models(
    adventure: Adventure,
    session: Session,
):
    content = AdventureInfo.model_validate_json(adventure.content)
    extra_info = {
        "nameLocation": content.location,
        "nameSetting": content.setting,
        "playerNum": str(content.playerNum),
        "playerNumXthree": str(content.playerNum * 3),
    }
    messages = _make_chat_logs(content)
    for tries in range(5):
        out_try, _ = _generate_iterative_chat(
            [characters_regeneration_prompts], extra_info, messages
        )
        if len(out_try) == 1:
            print(out)
            content.characters = [
                Character(name=x["name"], description=x["description"])
                for x in out_try[0]["players"]
            ]
            adventure = update_state_content_adventure(
                adventure.id, AdventureState.image_characters, content, session
            )
            generate_images_characters(adventure, session, state=AdventureState.ready)
        else:
            print(tries, "try of generation")
    print(messages)
    raise Exception()


def regenerate_items_concrete_with_models(
    adventure: Adventure,
    index_item: int,
    session: Session,
):
    content = AdventureInfo.model_validate_json(adventure.content)
    extra_info = {
        "nameLocation": content.location,
        "nameSetting": content.setting,
        "playerNum": str(content.playerNum),
        "playerNumXthree": str(content.playerNum * 3),
    }
    messages = _make_chat_logs(content)
    for tries in range(5):
        out_try, _ = _generate_iterative_chat(
            [items_regeneration_concrete_prompt], extra_info, messages
        )
        if len(out_try) == 1:
            print(out)
            content.items[index_item] = Item(
                name=out_try[0]["name"], description=out_try[0]["description"]
            )
            adventure = update_state_content_adventure(
                adventure.id, AdventureState.image_items, content, session
            )
            generate_images_items(adventure, session, state=AdventureState.ready)
        else:
            print(tries, "try of generation")
    print(messages)
    raise Exception()


def regenerate_items_with_models(
    adventure: Adventure,
    session: Session,
):
    content = AdventureInfo.model_validate_json(adventure.content)
    extra_info = {
        "nameLocation": content.location,
        "nameSetting": content.setting,
        "playerNum": str(content.playerNum),
        "playerNumXthree": str(content.playerNum * 3),
    }
    messages = _make_chat_logs(content)
    for tries in range(5):
        out_try, _ = _generate_iterative_chat(
            [items_regeneration_prompt], extra_info, messages
        )
        if len(out_try) == 1:
            print(out)
            content.items = [
                Item(name=x["name"], description=x["description"])
                for x in out_try[0]["items"]
            ]
            adventure = update_state_content_adventure(
                adventure.id, AdventureState.image_items, content, session
            )
            generate_images_items(adventure, session, state=AdventureState.ready)
        else:
            print(tries, "try of generation")
    print(messages)
    raise Exception()
