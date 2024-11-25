from abc import ABC, abstractmethod

from app.adventure.models import Adventure
import app.generation.prompts as prompts_template

from typing import final

import json

from app.adventure.schemas import *
from app.generation.schemas import *


def calc_default_config(adventure: AdventureInfo) -> dict[str, str]:
    return {
        "nameLocation": adventure.location,
        "nameSetting": adventure.setting,
        "playerNum": str(adventure.playerNum),
        "playerNumXthree": str(adventure.playerNum * 3),
    }


def calc_description_answer_config(adventure: AdventureInfo) -> dict[str, str]:
    description = {(i + 1): x for i, x in enumerate(adventure.description)}
    return {"description_json_answer": json.dumps(description, indent=4)}


def calc_items_answer_config(adventure: AdventureInfo) -> dict[str, str]:
    items = {
        "items": [
            {"name": x.name, "description": x.description} for x in adventure.items
        ]
    }
    return {"items_json_answer": json.dumps(items, indent=4)}


def calc_characters_answer_config(adventure: AdventureInfo) -> dict[str, str]:
    characters = {
        "players": [
            {"name": x.name, "description": x.description} for x in adventure.characters
        ]
    }
    return {"characters_json_answer": json.dumps(characters, indent=4)}


class TextGenerationInstruction(ABC):
    """
    Абстрактный класс для текстовых инструкции.
    """

    @abstractmethod
    def get_prompts(self) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_config(self, adventure: AdventureInfo) -> dict[str, str]:
        """
        Получить конфиг, который будет подставлять значения в промпт. Например 'nameLocation' содержит название локации.

        :param adventure - приключение на основе, которого генерится конфиг.
        """
        raise NotImplementedError()

    @abstractmethod
    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        raise NotImplementedError()


@final
class AdventureInfoInstruction(TextGenerationInstruction):
    """
    Класс инструкции для генерация описания всего приключения.
    """

    def get_prompts(self) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return prompts_template.adventure_info_prompts_messages

    def get_config(self, adventure: AdventureInfo) -> dict[str, str]:
        """
        Получить конфиг, который будет подставлять значения в промпт. Например 'nameLocation' содержит название локации.

        :param adventure - приключение на основе, которого генерится конфиг.
        """
        return calc_default_config(adventure)

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        generated_answer = AdventureInfoInstructionAnswer.model_validate(result)
        generated_description = generated_answer.description
        if type(generated_description) is str:
            adventure.description = generated_description.split("/n")
        elif type(generated_description) is list:
            adventure.description = generated_description
        elif type(generated_description) is dict:
            adventure.description = list(generated_description.values())
        return adventure


@final
class ItemsInstruction(TextGenerationInstruction):
    """
    Класс инструкции для генерация текстового описания предметов.
    """

    def get_prompts(self) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return prompts_template.items_prompts_messages

    def get_config(self, adventure: AdventureInfo) -> dict[str, str]:
        """
        Получить конфиг, который будет подставлять значения в промпт. Например 'nameLocation' содержит название локации.

        :param adventure - приключение на основе, которого генерится конфиг.
        """
        config = calc_default_config(adventure)
        config.update(calc_description_answer_config(adventure))
        return config

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        generated_answer = ItemInstructionAnswer.model_validate(result)
        adventure.items = [
            Item(name=x.name, description=x.description) for x in generated_answer.items
        ]
        return adventure


@final
class CharactersInstruction(TextGenerationInstruction):
    """
    Класс инструкции для генерация текстового описания персонажей.
    """

    def get_prompts(self) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return prompts_template.characters_prompts_messages

    def get_config(self, adventure: AdventureInfo) -> dict[str, str]:
        """
        Получить конфиг, который будет подставлять значения в промпт. Например 'nameLocation' содержит название локации.

        :param adventure - приключение на основе, которого генерится конфиг.
        """
        config = calc_default_config(adventure)
        config.update(calc_description_answer_config(adventure))
        config.update(calc_items_answer_config(adventure))
        return config

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        generated_answer = CharactersInstructionAnswer.model_validate(result)
        adventure.characters = [
            Character(name=x.name, description=x.description)
            for x in generated_answer.players
        ]
        return adventure


@final
class QuestsInstruction(TextGenerationInstruction):
    """
    Класс инструкции для генерация текстового описания квестов.
    """

    def get_prompts(self) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return prompts_template.quests_prompts_messages

    def get_config(self, adventure: AdventureInfo) -> dict[str, str]:
        """
        Получить конфиг, который будет подставлять значения в промпт. Например 'nameLocation' содержит название локации.

        :param adventure - приключение на основе, которого генерится конфиг.
        """
        config = calc_default_config(adventure)
        config.update(calc_description_answer_config(adventure))
        config.update(calc_items_answer_config(adventure))
        config.update(calc_characters_answer_config(adventure))
        return config

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        generated_answer = QuestsInstructionAnswer.model_validate(result)
        adventure.quests = [
            Quest(name=x.name, description=x.description, goal=x.goal)
            for x in generated_answer.quests
        ]
        return adventure


# ============================= QUESTS ========================


@final
class QuestsRegenerateInstruction(TextGenerationInstruction):
    """
    Класс инструкции для перегенерация текстового описания всех квестов.
    """

    def get_prompts(self) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return prompts_template.quests_regenerate_prompts_messages

    def get_config(self, adventure: AdventureInfo) -> dict[str, str]:
        """
        Получить конфиг, который будет подставлять значения в промпт. Например 'nameLocation' содержит название локации.

        :param adventure - приключение на основе, которого генерится конфиг.
        """
        config = calc_default_config(adventure)
        config.update(calc_description_answer_config(adventure))
        config.update(calc_items_answer_config(adventure))
        config.update(calc_characters_answer_config(adventure))
        return config

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        raise NotImplementedError()


@final
class QuestsConcreteRegenerateInstruction(TextGenerationInstruction):
    """
    Класс инструкции для перегенерация текстового описания конкретного квеста.
    """

    index: int

    def __init__(self, index: int):
        self.index = index

    def get_prompts(self) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return prompts_template.quests_concrete_regenerate_prompts_messages

    def get_config(self, adventure: AdventureInfo) -> dict[str, str]:
        """
        Получить конфиг, который будет подставлять значения в промпт. Например 'nameLocation' содержит название локации.

        :param adventure - приключение на основе, которого генерится конфиг.
        """
        config = calc_default_config(adventure)
        config.update(calc_description_answer_config(adventure))
        config.update(calc_items_answer_config(adventure))
        config.update(calc_characters_answer_config(adventure))
        return config

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        raise NotImplementedError()


# ================================ CHARACTERS ===========================


@final
class CharactersRegenerateInstruction(TextGenerationInstruction):
    """
    Класс инструкции для перегенерация текстового описания всех персонажей.
    """

    def get_prompts(self) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return prompts_template.characters_regenerate_prompts_messages

    def get_config(self, adventure: AdventureInfo) -> dict[str, str]:
        """
        Получить конфиг, который будет подставлять значения в промпт. Например 'nameLocation' содержит название локации.

        :param adventure - приключение на основе, которого генерится конфиг.
        """
        config = calc_default_config(adventure)
        config.update(calc_description_answer_config(adventure))
        config.update(calc_items_answer_config(adventure))
        config.update(calc_characters_answer_config(adventure))
        return config

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        raise NotImplementedError()


@final
class CharactersConcreteRegenerateInstruction(TextGenerationInstruction):
    """
    Класс инструкции для перегенерация текстового описания конкретного персонажа.
    """

    index: int

    def __init__(self, index: int):
        self.index = index

    def get_prompts(self) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return prompts_template.characters_concrete_regenerate_prompts_messages

    def get_config(self, adventure: AdventureInfo) -> dict[str, str]:
        """
        Получить конфиг, который будет подставлять значения в промпт. Например 'nameLocation' содержит название локации.

        :param adventure - приключение на основе, которого генерится конфиг.
        """
        config = calc_default_config(adventure)
        config.update(calc_description_answer_config(adventure))
        config.update(calc_items_answer_config(adventure))
        config.update(calc_characters_answer_config(adventure))
        return config

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        raise NotImplementedError()


# ================================== ITEMS ======================================


@final
class ItemsRegenerateInstruction(TextGenerationInstruction):
    """
    Класс инструкции для перегенерация текстового описания всех предметов.
    """

    def get_prompts(self) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return prompts_template.items_regenerate_prompts_messages

    def get_config(self, adventure: AdventureInfo) -> dict[str, str]:
        """
        Получить конфиг, который будет подставлять значения в промпт. Например 'nameLocation' содержит название локации.

        :param adventure - приключение на основе, которого генерится конфиг.
        """
        config = calc_default_config(adventure)
        config.update(calc_description_answer_config(adventure))
        config.update(calc_items_answer_config(adventure))
        config.update(calc_characters_answer_config(adventure))
        return config

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        raise NotImplementedError()


@final
class ItemsConcreteRegenerateInstruction(TextGenerationInstruction):
    """
    Класс инструкции для перегенерация текстового описания конкретного предмета.
    """

    index: int

    def __init__(self, index: int):
        self.index = index

    def get_prompts(self) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return prompts_template.items_concrete_regenerate_prompts_messages

    def get_config(self, adventure: AdventureInfo) -> dict[str, str]:
        """
        Получить конфиг, который будет подставлять значения в промпт. Например 'nameLocation' содержит название локации.

        :param adventure - приключение на основе, которого генерится конфиг.
        """
        config = calc_default_config(adventure)
        config.update(calc_description_answer_config(adventure))
        config.update(calc_items_answer_config(adventure))
        config.update(calc_characters_answer_config(adventure))
        return config

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        raise NotImplementedError()
