from typing import Any
from pydantic import BaseModel
from enum import Enum


class AdventureInfoInstructionAnswer(BaseModel):
    description: dict[int|str, str] | list[str] | str


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


class MessageType(Enum):
    assistant = 0
    user = 1
    system = 2

class Message(BaseModel):
    type: MessageType
    content: str

class TextGenerationResult(BaseModel):
    content: str
    prompt_token_count: int
    assistant_token_count: int

class JSONGenerationResult(BaseModel):
    content: dict[str, Any]
    prompt_token_count: int
    assistant_token_count: int