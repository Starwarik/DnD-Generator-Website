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


class TextGenerationResult(BaseModel):
    """
    Текстовый результат модели.
    * content - текст сообщений.
    * prompt_token_count - кол-во токенов инструкции, потраченных на генерацию.
    * assistant_token_count - кол-во токенов, которые сгенерировала модель.
    """
    content: str
    prompt_token_count: int
    assistant_token_count: int


class JSONGenerationResult(BaseModel):
    """
    Json результат модели.
    * content - результат в виде словаря.
    * prompt_token_count - кол-во токенов инструкции, потраченных на генерацию.
    * assistant_token_count - кол-во токенов, которые сгенерировала модель.
    """
    content: dict[str, Any]
    prompt_token_count: int
    assistant_token_count: int

# ======================== Ответы для инструкций ==============================

class AdventureInfoInstructionAnswer(BaseModel):
    description: dict[int | str, str] | list[str] | str


class ItemAnswer(BaseModel):
    name: str
    description: str


class ItemInstructionAnswer(BaseModel):
    items: list[ItemAnswer]


class CharacterAnswer(BaseModel):
    name: str
    description: str


class CharactersInstructionAnswer(BaseModel):
    players: list[CharacterAnswer]


class QuestAnswer(BaseModel):
    name: str
    description: str
    goal: str


class QuestsInstructionAnswer(BaseModel):
    quests: list[QuestAnswer]
