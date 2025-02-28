from abc import ABC, abstractmethod
import json

import worker.text_tasks.prompts as prompts_template

from typing import final, Any

from copy import deepcopy

from worker.database.schemas import *
from worker.text_tasks.schemas import *


class RegenerationType(Enum):
    none = 0
    items = 1
    items_concrete = 2
    npc = 3
    npc_concrete = 4
    quest = 5
    quest_concrete = 6

class ContextConfig(BaseModel):
    include_adventure_info: bool = False
    include_items: bool = False
    include_npcs: bool = False
    include_quests: bool = False
    include_regeneration: RegenerationType = RegenerationType.none
    index_regeneration: int | None = None


def calc_default_context(adventure: AdventureInfo) -> dict[str, str]:
    return {
        "nameLocation": adventure.location,
        "nameSetting": adventure.setting,
        "playerNum": str(adventure.playerNum),
        "playerNumXthree": str(adventure.playerNum * 3),
    }


def calc_description_answer_context(adventure: AdventureInfo) -> dict[str, str]:
    return {
        "description_json_answer": AdventureInfoInstructionAnswer.model_validate(
            adventure, from_attributes=True
        ).model_dump_json(indent=4)
    }


def calc_items_answer_context(adventure: AdventureInfo) -> dict[str, str]:
    items = [
        ItemAnswer.model_validate(x, from_attributes=True) for x in adventure.items
    ]
    return {
        "items_json_answer": ItemInstructionAnswer(items=items).model_dump_json(
            indent=4
        )
    }


def calc_npcs_answer_context(adventure: AdventureInfo) -> dict[str, str]:
    npc = [NPCAnswer.model_validate(x, from_attributes=True) for x in adventure.npcs]
    return {
        "characters_json_answer": NPCsInstructionAnswer(npc=npc).model_dump_json(
            indent=4
        )
    }


def calc_quest_answer_context(adventure: AdventureInfo) -> dict[str, str]:
    quests = [
        QuestAnswer.model_validate(x, from_attributes=True) for x in adventure.quests
    ]
    return {
        "quests_json_answer": json.dumps([q.model_dump() for q in quests], indent=4)
    }

def implement_context(message: Message, context: dict[str, str]):
    new_message = deepcopy(message)
    new_message.content = new_message.content.format(**context)
    return new_message

def create_context(adventure: AdventureInfo):
    context = calc_default_context(adventure)
    if adventure.description_location != "" and len(adventure.description_places) != 0:
        context.update(calc_description_answer_context(adventure))
    if len(adventure.items) != 0:
        context.update(calc_items_answer_context(adventure))
    if len(adventure.npcs) != 0:
        context.update(calc_npcs_answer_context(adventure))
    if len(adventure.quests) != 0:
        context.update(calc_quest_answer_context(adventure))
    return context

def create_prompts(adventure: AdventureInfo, config: ContextConfig):
    prompt: list[Message] = []
    context = create_context(adventure)
    if config.include_adventure_info:
        prompt.append(implement_context(prompts_template.adventure_info_prompt, context))
        if "description_json_answer" in context:
            prompt.append(implement_context(prompts_template.adventure_info_answer, context))
    if config.include_items:
        prompt.append(implement_context(prompts_template.items_prompt, context))
        if "items_json_answer" in context:
            prompt.append(implement_context(prompts_template.items_answer, context))
    if config.include_npcs:
        prompt.append(implement_context(prompts_template.npcs_prompt, context))
        if "characters_json_answer" in context:
            prompt.append(implement_context(prompts_template.npcs_answer, context))
    if config.include_quests:
        prompt.append(implement_context(prompts_template.quests_prompt, context))
        if "quests_json_answer" in context:
            prompt.append(implement_context(prompts_template.quests_answer, context))
    match config.include_regeneration:
        case RegenerationType.none:
            pass
        case RegenerationType.items:
            prompt.append(implement_context(prompts_template.items_regeneration_prompt, context))
        case RegenerationType.items_concrete:
            assert config.index_regeneration
            item = adventure.items[config.index_regeneration]
            context.update(nameItem=item.name)
            prompt.append(implement_context(prompts_template.items_regeneration_concrete_prompt, context))
        case RegenerationType.npc:
            prompt.append(implement_context(prompts_template.npcs_regeneration_prompt, context))
        case RegenerationType.npc_concrete:
            assert config.index_regeneration
            npc = adventure.npcs[config.index_regeneration]
            context.update(nameNPC=npc.name)
            prompt.append(implement_context(prompts_template.npcs_regeneration_concrete_prompt, context))
        case RegenerationType.quest:
            prompt.append(implement_context(prompts_template.quests_regeneration_prompt, context))
        case RegenerationType.quest_concrete:
            assert config.index_regeneration
            quest = adventure.quests[config.index_regeneration]
            context.update(name_quest=quest.name)
            prompt.append(implement_context(prompts_template.quests_regeneration_concrete_prompt, context))
    return prompt


class TextGenerationInstruction(ABC):
    """
    Абстрактный класс для текстовых инструкции.
    """

    @abstractmethod
    def get_prompts(self, adventure: AdventureInfo) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
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

    def get_prompts(self, adventure: AdventureInfo) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return create_prompts(adventure, ContextConfig(include_adventure_info=True))

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
        adventure.annotation = generated_answer.description_location.split(".")[0]
        return adventure


@final
class ItemsInstruction(TextGenerationInstruction):
    """
    Класс инструкции для генерация текстового описания предметов.
    """

    def get_prompts(self, adventure: AdventureInfo) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return create_prompts(adventure, ContextConfig(include_adventure_info=True, include_items=True))
    
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

    def get_prompts(self, adventure: AdventureInfo) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return create_prompts(adventure, ContextConfig(include_adventure_info=True, include_items=True, include_npcs=True))

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

    def get_prompts(self, adventure: AdventureInfo) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return create_prompts(adventure, ContextConfig(include_adventure_info=True, include_items=True, include_npcs=True, include_quests=True))

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: list[dict[str, Any]] | dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        if isinstance(result, dict):
            result = result["quests"]
        adventure.quests = [Quest.model_validate(x) for x in result]
        for i in range(len(adventure.quests)):
            adventure.quests[i].id_quest = i
        return adventure


# ============================= QUESTS ========================


@final
class QuestsRegenerateInstruction(TextGenerationInstruction):
    """
    Класс инструкции для перегенерация текстового описания всех квестов.
    """

    def get_prompts(self, adventure: AdventureInfo) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return create_prompts(
            adventure,
            ContextConfig(include_adventure_info=True, include_items=True, include_npcs=True, include_regeneration=RegenerationType.quest)
        )

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: list[dict[str, Any]] | dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        if isinstance(result, dict):
            result = result["quests"]
        adventure.quests = [Quest.model_validate(x) for x in result]
        for i in range(len(adventure.quests)):
            adventure.quests[i].id_quest = i
        return adventure


@final
class QuestsConcreteRegenerateInstruction(TextGenerationInstruction):
    """
    Класс инструкции для перегенерация текстового описания конкретного квеста.
    """

    index: int

    def __init__(self, index: int):
        self.index = index

    def get_prompts(self, adventure: AdventureInfo) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return create_prompts(
            adventure,
            ContextConfig(
                include_adventure_info=True,
                include_items=True,
                include_npcs=True,
                include_regeneration=RegenerationType.quest_concrete,
                index_regeneration=self.index
            )
        )

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        generated_answer: QuestInstructionConcreteAnswer = QuestInstructionConcreteAnswer.model_validate(result)
        if type(generated_answer.quests) is list:
            quest = Quest.model_validate(generated_answer.quests[0], from_attributes=True)
        else:
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

    def get_prompts(self, adventure: AdventureInfo) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return create_prompts(
            adventure,
            ContextConfig(include_adventure_info=True, include_items=True, include_quests=True, include_regeneration=RegenerationType.npc)
        )

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

    def get_prompts(self, adventure: AdventureInfo) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return create_prompts(
            adventure,
            ContextConfig(
                include_adventure_info=True,
                include_items=True,
                include_quests=True,
                include_regeneration=RegenerationType.npc_concrete,
                index_regeneration=self.index
            )
        )

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        generated_answer = NPCInstructionConcreteAnswer.model_validate(result)
        if type(generated_answer.npc) is list:
            npc = NPC.model_validate(generated_answer.npc[0], from_attributes=True)
        else:
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

    def get_prompts(self, adventure: AdventureInfo) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return create_prompts(
            adventure,
            ContextConfig(include_adventure_info=True, include_npcs=True, include_quests=True, include_regeneration=RegenerationType.items)
        )

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

    def get_prompts(self, adventure: AdventureInfo) -> list[Message]:
        """
        Получает промпты, по которым будет производится генерация.
        """
        return create_prompts(
            adventure,
            ContextConfig(
                include_adventure_info=True,
                include_npcs=True,
                include_quests=True,
                include_regeneration=RegenerationType.items_concrete,
                index_regeneration=self.index
            )
        )

    def change_adventure_on_success(
        self, adventure: AdventureInfo, result: dict[str, Any]
    ) -> AdventureInfo:
        """
        Получает результат генерации и изменяет приключение.

        :param adventure - информация о приключении
        :param result - результат генерации
        """
        generated_answer = ItemInstructionConcreteAnswer.model_validate(result)
        if type(generated_answer.items) is list:
            item = Item.model_validate(generated_answer.items[0], from_attributes=True)
        else:
            item = Item.model_validate(generated_answer.items, from_attributes=True)
        item.id_items = self.index
        adventure.items[self.index] = item
        return adventure
