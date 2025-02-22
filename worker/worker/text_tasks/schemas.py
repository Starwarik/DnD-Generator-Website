from pydantic import BaseModel
from enum import Enum
from worker.database.schemas import SpentedTokensCounts


class MessageType(Enum):
    assistant = 0
    user = 1
    system = 2


def message_type2str(x: MessageType):
    if x == MessageType.assistant:
        return "Assistant"
    if x == MessageType.user:
        return "User"
    return "System"


class Message(BaseModel):
    """
    Сообщение в чате с моделью.
    """

    type: MessageType
    content: str

    def __repr__(self):
        return f"{message_type2str(self.type)}: {self.content}"

    def __str__(self):
        return self.__repr__()


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
    description_location: str
    description_places: list[str]


class ItemAnswer(BaseModel):
    name: str
    description: str
    values: str
    type: str
    damage: str | None = None
    armor_class: str | None = None


class ItemInstructionAnswer(BaseModel):
    items: list[ItemAnswer]


class NPCAnswer(BaseModel):
    name: str
    disc_costum: str
    dic_life: str


class NPCsInstructionAnswer(BaseModel):
    npc: list[NPCAnswer]

class QuestRewards(BaseModel):
    gold: str
    silver: str
    bronze: str


class QuestAnswer(BaseModel):
    name: str
    description: str
    goal: str
    rewards: QuestRewards


class QuestsInstructionAnswer(BaseModel):
    quests: list[QuestAnswer]


class QuestInstructionConcreteAnswer(BaseModel):
    quests: QuestAnswer | list[QuestAnswer]


class NPCInstructionConcreteAnswer(BaseModel):
    npc: NPCAnswer | list[NPCAnswer]


class ItemInstructionConcreteAnswer(BaseModel):
    items: ItemAnswer | list[ItemAnswer]
