from typing import Any
from app.adventure.schemas import *
from app.generation.instructions import *
from app.generation.text_models import TextGenerationModel
from app.generation.schemas import JSONGenerationResult
import json
from sqlalchemy.orm import Session
from app.adventure.models import Adventure, AdventureState
from app.adventure.service import create_adventure, update_state_content_adventure

class MaxAttemptsExced(Exception):
    pass

def parse_json_garbage(s: str) -> dict[str, Any]:
    """
    Пытается найти json среди str. Если не получается возращает ошибку JSONDecodeError.
    """
    s = s[next(idx for idx, c in enumerate(s) if c in "{[") :]
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        try:
            return json.loads(s[: e.pos])
        except Exception as e:
            print(s)
            raise e


def generate_text_with_tries(
    instructions: list[TextGenerationInstruction],
    adventure: AdventureInfo,
    model: TextGenerationModel,
    n_tries: int = 3,
) -> AdventureInfo:
    """
    Изменение информации приключения по данным инструкциям. На выходе выдает новое приключение.

    :param instructions: Инструкции, по которым будет меняться приключение.
    :param adventure: Изначальное содержание приключения.
    :param model: модель для генрации текста
    :param n_tries: количество попыток генерации перед выбросом ошибки.
    """
    for instruction in instructions:
        prompts = instruction.get_prompts()
        config = instruction.get_config(adventure)
        for i in range(len(prompts)):
            prompts[i].content = prompts[i].content.format(**config)
        generated_result = None
        for _ in range(n_tries):
            try:
                generated_result = model.generate_text(prompts)
            except Exception as e:
                print(_, "try failed")
                print(e)
        if generated_result is None:
            raise MaxAttemptsExced("Max tries")
        print("Success")
        generated_json = JSONGenerationResult(
            content=parse_json_garbage(generated_result.content),
            prompt_token_count=generated_result.prompt_token_count,
            assistant_token_count=generated_result.assistant_token_count,
        )
        print(generated_json)
        adventure = instruction.change_adventure_on_success(adventure, generated_json)
    return adventure


def generate_new_adventure_json(
    location_name: str,
    setting: str,
    num_players: int,
    model: TextGenerationModel,
    adventure: Adventure,
    session: Session,
) -> Adventure:
    """
    Генерирует полноценное приключение с нуля.

    :param location_name: название локации
    :param setting: сеттинг
    :param num_players: кол-во игроков
    :param model: модель для генерации текста
    :param adventure: модель приключения из бд
    :param session: для бд
    """

    adventure_info = AdventureInfo(
        name=location_name,
        location=location_name,
        setting=setting,
        playerNum=num_players,
        annotation="",
        description=[],
        characters=[],
        items=[],
        quests=[],
    )

    instructions: list[TextGenerationInstruction] = [
        AdventureInfoInstruction(),
        ItemsInstruction(),
        CharactersInstruction(),
        QuestsInstruction(),
    ]

    adventure_info = generate_text_with_tries(instructions, adventure_info, model)
    adventure = update_state_content_adventure(
        adventure.id, AdventureState.image_adventure, adventure_info, session
    )
    return adventure


def generate_new_test_adventure_json(
    location_name: str,
    setting: str,
    num_players: int,
    adventure: Adventure,
    session: Session,
) -> Adventure:
    """
    Генерирует фиктивное приключение для тестирования.
    :param location_name: название локации
    :param setting: сеттинг
    :param num_players: кол-во игроков
    :param adventure: модель приключения из бд
    :param session: для бд
    """

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
    adventure = update_state_content_adventure(
        adventure.id, AdventureState.image_adventure, adventure_info, session
    )
    return adventure


def regenerate_new_adventure_json(
    adventure: Adventure, model: TextGenerationModel, session: Session
) -> Adventure:
    """
    Перегенерировать всё приключение заново.

    :param adventure: модель приключения из бд
    :param model: модель для генерации текста
    :param session: для бд
    """
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    adventure_info = AdventureInfo(
        name=adventure_info.location,
        location=adventure_info.location,
        setting=adventure_info.setting,
        playerNum=adventure_info.playerNum,
        annotation="",
        description=[],
        characters=[],
        items=[],
        quests=[],
    )

    instructions: list[TextGenerationInstruction] = [
        AdventureInfoInstruction(),
        ItemsInstruction(),
        CharactersInstruction(),
        QuestsInstruction(),
    ]

    adventure_info = generate_text_with_tries(instructions, adventure_info, model)
    adventure = update_state_content_adventure(
        adventure.id, AdventureState.image_adventure, adventure_info, session
    )
    return adventure


# ============================= QUESTS ========================


def regenerate_quests_json(
    adventure: Adventure, model: TextGenerationModel, session: Session
) -> Adventure:
    """
    Перегенерировать все квесты заново. Только текстовое содержание.

    :param adventure: модель приключения из бд
    :param model: модель для генерации текста
    :param session: для бд
    """
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    instructions: list[TextGenerationInstruction] = [QuestsRegenerateInstruction()]
    adventure_info = generate_text_with_tries(instructions, adventure_info, model)
    adventure = update_state_content_adventure(
        adventure.id, AdventureState.ready, adventure_info, session
    )
    return adventure


def regenerate_quest_concrete_json(
    index_quest: int, adventure: Adventure, model: TextGenerationModel, session: Session
) -> Adventure:
    """
    Перегенерировать конкретный квест заново. Только текстовое содержание.

    :param index_quest: индекс квеста, которого нужно перегенерировать.
    :param adventure: модель приключения из бд
    :param model: модель для генерации текста
    :param session: для бд
    """
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    instructions: list[TextGenerationInstruction] = [
        QuestsConcreteRegenerateInstruction(index_quest)
    ]
    adventure_info = generate_text_with_tries(instructions, adventure_info, model)
    adventure = update_state_content_adventure(
        adventure.id, AdventureState.ready, adventure_info, session
    )
    return adventure


# ================================ CHARACTERS ===========================


def regenerate_characters_json(
    adventure: Adventure, model: TextGenerationModel, session: Session
) -> Adventure:
    """
    Перегенерировать всех персонажей заново. Только текстовое содержание.

    :param adventure: модель приключения из бд
    :param model: модель для генерации текста
    :param session: для бд
    """
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    instructions: list[TextGenerationInstruction] = [CharactersRegenerateInstruction()]
    adventure_info = generate_text_with_tries(instructions, adventure_info, model)
    adventure = update_state_content_adventure(
        adventure.id, AdventureState.image_characters, adventure_info, session
    )
    return adventure


def regenerate_character_concrete_json(
    index_character: int,
    adventure: Adventure,
    model: TextGenerationModel,
    session: Session,
) -> Adventure:
    """
    Перегенерировать конкретный персонажа заново. Только текстовое содержание.

    :param index_character: индекс персонажа, которого нужно перегенерировать.
    :param adventure: модель приключения из бд
    :param model: модель для генерации текста
    :param session: для бд
    """
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    instructions: list[TextGenerationInstruction] = [
        CharactersConcreteRegenerateInstruction(index_character)
    ]
    adventure_info = generate_text_with_tries(instructions, adventure_info, model)
    adventure = update_state_content_adventure(
        adventure.id, AdventureState.image_characters, adventure_info, session
    )
    return adventure


# ================================== ITEMS ======================================


def regenerate_items_json(
    adventure: Adventure, model: TextGenerationModel, session: Session
) -> Adventure:
    """
    Перегенерировать все предметы заново. Только текстовое содержание.

    :param adventure: модель приключения из бд
    :param model: модель для генерации текста
    :param session: для бд
    """
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    instructions: list[TextGenerationInstruction] = [ItemsRegenerateInstruction()]
    adventure_info = generate_text_with_tries(instructions, adventure_info, model)
    adventure = update_state_content_adventure(
        adventure.id, AdventureState.image_items, adventure_info, session
    )
    return adventure


def regenerate_item_concrete_json(
    index_item: int, adventure: Adventure, model: TextGenerationModel, session: Session
) -> Adventure:
    """
    Перегенерировать конкретный предмет заново. Только текстовое содержание.

    :param index_item: индекс предмет, которого нужно перегенерировать.
    :param adventure: модель приключения из бд
    :param model: модель для генерации текста
    :param session: для бд
    """
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    instructions: list[TextGenerationInstruction] = [
        ItemsConcreteRegenerateInstruction(index_item)
    ]
    adventure_info = generate_text_with_tries(instructions, adventure_info, model)
    adventure = update_state_content_adventure(
        adventure.id, AdventureState.image_items, adventure_info, session
    )
    return adventure
