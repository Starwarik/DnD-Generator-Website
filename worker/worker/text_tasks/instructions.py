from abc import ABC, abstractmethod

import worker.text_tasks.prompts as prompts_template

from typing import final, Any

from copy import deepcopy

from worker.database.schemas import *
from worker.text_tasks.schemas import *


def calc_default_config(adventure: AdventureInfo) -> dict[str, str]:
    return {
        "nameLocation": adventure.location,
        "nameSetting": adventure.setting,
        "playerNum": str(adventure.playerNum),
        "playerNumXthree": str(adventure.playerNum * 3),
    }


def calc_description_answer_config(adventure: AdventureInfo) -> dict[str, str]:
    return {
        "description_json_answer": AdventureInfoInstructionAnswer.model_validate(
            adventure, from_attributes=True
        ).model_dump_json(indent=4)
    }


def calc_items_answer_config(adventure: AdventureInfo) -> dict[str, str]:
    items = [
        ItemAnswer.model_validate(x, from_attributes=True) for x in adventure.items
    ]
    return {
        "items_json_answer": ItemInstructionAnswer(items=items).model_dump_json(
            indent=4
        )
    }


def calc_npcs_answer_config(adventure: AdventureInfo) -> dict[str, str]:
    npc = [NPCAnswer.model_validate(x, from_attributes=True) for x in adventure.npcs]
    return {
        "characters_json_answer": NPCsInstructionAnswer(npc=npc).model_dump_json(
            indent=4
        )
    }


def calc_quest_answer_config(adventure: AdventureInfo) -> dict[str, str]:
    quests = [
        QuestAnswer.model_validate(x, from_attributes=True) for x in adventure.quests
    ]
    return {
        "quests_json_answer": QuestsInstructionAnswer(quests=quests).model_dump_json(
            indent=4
        )
    }


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
        return deepcopy(prompts_template.adventure_info_prompts_messages)

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
        generated_answer = AdventureInfoInstructionAnswer.model_validate(
            result["location"]
        )
        adventure.description_location = generated_answer.description_location
        adventure.description_places = generated_answer.description_places
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
        return deepcopy(prompts_template.items_prompts_messages)

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
            Item.model_validate(x, from_attributes=True) for x in generated_answer.items
        ]
        for i in range(len(adventure.items)):
            adventure.items[i].id_items = i
        return adventure


@final
class NPCsInstruction(TextGenerationInstruction):
    """
    Класс инструкции для генерация текстового описания персонажей.
    """

    def get_prompts(self) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return deepcopy(prompts_template.npcs_prompts_messages)

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
        generated_answer = NPCsInstructionAnswer.model_validate(result)

        adventure.npcs = [
            NPC.model_validate(x, from_attributes=True) for x in generated_answer.npc
        ]
        for i in range(len(adventure.npcs)):
            adventure.npcs[i].id_npc = i
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
        return deepcopy(prompts_template.quests_prompts_messages)

    def get_config(self, adventure: AdventureInfo) -> dict[str, str]:
        """
        Получить конфиг, который будет подставлять значения в промпт. Например 'nameLocation' содержит название локации.

        :param adventure - приключение на основе, которого генерится конфиг.
        """
        config = calc_default_config(adventure)
        config.update(calc_description_answer_config(adventure))
        config.update(calc_items_answer_config(adventure))
        config.update(calc_npcs_answer_config(adventure))
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
            Quest.model_validate(x, from_attributes=True)
            for x in generated_answer.quests
        ]
        for i in range(len(adventure.quests)):
            adventure.quests[i].id_quest = i
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
        return deepcopy(prompts_template.quests_regenerate_prompts_messages)

    def get_config(self, adventure: AdventureInfo) -> dict[str, str]:
        """
        Получить конфиг, который будет подставлять значения в промпт. Например 'nameLocation' содержит название локации.

        :param adventure - приключение на основе, которого генерится конфиг.
        """
        config = calc_default_config(adventure)
        config.update(calc_description_answer_config(adventure))
        config.update(calc_items_answer_config(adventure))
        config.update(calc_npcs_answer_config(adventure))
        config.update(calc_quest_answer_config(adventure))
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
            Quest.model_validate(x, from_attributes=True)
            for x in generated_answer.quests
        ]
        for i in range(len(adventure.quests)):
            adventure.quests[i].id_quest = i
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
        return deepcopy(prompts_template.quests_concrete_regenerate_prompts_messages)

    def get_config(self, adventure: AdventureInfo) -> dict[str, str]:
        """
        Получить конфиг, который будет подставлять значения в промпт. Например 'nameLocation' содержит название локации.

        :param adventure - приключение на основе, которого генерится конфиг.
        """
        config = calc_default_config(adventure)
        config.update(calc_description_answer_config(adventure))
        config.update(calc_items_answer_config(adventure))
        config.update(calc_npcs_answer_config(adventure))
        config.update(calc_quest_answer_config(adventure))
        quest = adventure.quests[self.index]
        config.update(name_quest=quest.name)
        return config

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        generated_answer = QuestInstructionConcreteAnswer.model_validate(result)
        quest = Quest.model_validate(generated_answer.quests, from_attributes=True)
        quest.id_quest = self.index
        adventure.quests[self.index] = quest
        return adventure


# ================================ CHARACTERS ===========================


@final
class NPCsRegenerateInstruction(TextGenerationInstruction):
    """
    Класс инструкции для перегенерация текстового описания всех персонажей.
    """

    def get_prompts(self) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return deepcopy(prompts_template.npcs_regenerate_prompts_messages)

    def get_config(self, adventure: AdventureInfo) -> dict[str, str]:
        """
        Получить конфиг, который будет подставлять значения в промпт. Например 'nameLocation' содержит название локации.

        :param adventure - приключение на основе, которого генерится конфиг.
        """
        config = calc_default_config(adventure)
        config.update(calc_description_answer_config(adventure))
        config.update(calc_items_answer_config(adventure))
        config.update(calc_npcs_answer_config(adventure))
        config.update(calc_quest_answer_config(adventure))
        return config

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        generated_answer = NPCsInstructionAnswer.model_validate(result)
        adventure.npcs = [
            NPC.model_validate(x, from_attributes=True) for x in generated_answer.npc
        ]
        for i in range(len(adventure.npcs)):
            adventure.npcs[i].id_npc = i
        return adventure


@final
class NPCsConcreteRegenerateInstruction(TextGenerationInstruction):
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
        return deepcopy(prompts_template.npcs_concrete_regenerate_prompts_messages)

    def get_config(self, adventure: AdventureInfo) -> dict[str, str]:
        """
        Получить конфиг, который будет подставлять значения в промпт. Например 'nameLocation' содержит название локации.

        :param adventure - приключение на основе, которого генерится конфиг.
        """
        config = calc_default_config(adventure)
        config.update(calc_description_answer_config(adventure))
        config.update(calc_items_answer_config(adventure))
        config.update(calc_npcs_answer_config(adventure))
        config.update(calc_quest_answer_config(adventure))
        npc = adventure.quests[self.index]
        config.update(nameNPC=npc.name)
        return config

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        generated_answer = NPCInstructionConcreteAnswer.model_validate(result)
        npc = NPC.model_validate(generated_answer.npc, from_attributes=True)
        npc.id_npc = self.index
        adventure.npcs[self.index] = npc
        return adventure


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
        return deepcopy(prompts_template.items_regenerate_prompts_messages)

    def get_config(self, adventure: AdventureInfo) -> dict[str, str]:
        """
        Получить конфиг, который будет подставлять значения в промпт. Например 'nameLocation' содержит название локации.

        :param adventure - приключение на основе, которого генерится конфиг.
        """
        config = calc_default_config(adventure)
        config.update(calc_description_answer_config(adventure))
        config.update(calc_items_answer_config(adventure))
        config.update(calc_npcs_answer_config(adventure))
        config.update(calc_quest_answer_config(adventure))
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
            Item.model_validate(x, from_attributes=True) for x in generated_answer.items
        ]
        for i in range(len(adventure.items)):
            adventure.items[i].id_items = i
        return adventure


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
        return deepcopy(prompts_template.items_concrete_regenerate_prompts_messages)

    def get_config(self, adventure: AdventureInfo) -> dict[str, str]:
        """
        Получить конфиг, который будет подставлять значения в промпт. Например 'nameLocation' содержит название локации.

        :param adventure - приключение на основе, которого генерится конфиг.
        """
        config = calc_default_config(adventure)
        config.update(calc_description_answer_config(adventure))
        config.update(calc_items_answer_config(adventure))
        config.update(calc_npcs_answer_config(adventure))
        config.update(calc_quest_answer_config(adventure))
        item = adventure.items[self.index]
        config.update(nameItem=item.name)
        return config

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        generated_answer = ItemInstructionConcreteAnswer.model_validate(result)
        item = Item.model_validate(generated_answer.items, from_attributes=True)
        item.id_items = self.index
        adventure.items[self.index] = item
        return adventure
