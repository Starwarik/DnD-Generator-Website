from typing import Any
from pydantic import BaseModel
from enum import Enum


class MessageType(Enum):
    assistant = 0
    user = 1
    system = 2


class Message(BaseModel):
    """
    Сообщение в чате с моделью.
    """

    type: MessageType
    content: str


class SpentedTokensCounts(BaseModel):
    gigachat_prompt_token_count: int = 0
    gigachat_assistant_token_count: int = 0
    yandexgpt_prompt_token_count: int = 0
    yandexgpt_assistant_token_count: int = 0
    image_generated: int = 0

    def __add__(self, other):
        if not isinstance(other, SpentedTokensCounts):
            raise ValueError("Неправильный тип", str(type(other)))

        return SpentedTokensCounts(
            gigachat_prompt_token_count=self.gigachat_prompt_token_count
            + other.gigachat_prompt_token_count,
            gigachat_assistant_token_count=self.gigachat_assistant_token_count
            + other.gigachat_assistant_token_count,
            yandexgpt_prompt_token_count=self.yandexgpt_prompt_token_count
            + other.yandexgpt_prompt_token_count,
            yandexgpt_assistant_token_count=self.yandexgpt_assistant_token_count
            + other.yandexgpt_assistant_token_count,
            image_generated=self.image_generated + other.image_generated,
        )

    def __radd__(self, other):
        return self.__add__(other)


class TextGenerationResult(BaseModel):
    """
    Текстовый результат модели.
    * content - текст сообщений.
    * prompt_token_count - кол-во токенов инструкции, потраченных на генерацию.
    * assistant_token_count - кол-во токенов, которые сгенерировала модель.
    """

    content: str
    count_tokens: SpentedTokensCounts


# ======================== Ответы для инструкций ==============================


class AdventureInfoInstructionAnswer(BaseModel):
    name: str
    description_location: str
    description_quests: list[str]


class ItemAnswer(BaseModel):
    id_items: int
    name: str
    description: str
    values: str
    type: str
    damage: str | None
    armor_class: str | None


class ItemInstructionAnswer(BaseModel):
    items: list[ItemAnswer]


class CharacterAnswer(BaseModel):
    id_npc: str
    name: str
    disc_costum: str
    dic_life: str


class CharactersInstructionAnswer(BaseModel):
    npc: list[CharacterAnswer]


class QuestAnswer(BaseModel):
    name: str
    description: str
    goal: str


class QuestsInstructionAnswer(BaseModel):
    quests: list[QuestAnswer]
