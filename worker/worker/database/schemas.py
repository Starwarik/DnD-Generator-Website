from pydantic import BaseModel


class ImageContainer(BaseModel):
    content: bytes
    media_type: str


class NPC(BaseModel):
    id_npc: int | None = None
    name: str
    disc_costum: str
    dic_life: str
    image_id: int = -1


class Item(BaseModel):
    id_items: int | None = None
    name: str
    description: str
    values: str
    type: str
    damage: str | None
    armor_class: str | None
    image_id: int = -1


class QuestRewards(BaseModel):
    gold: int
    silver: int
    bronze: int

class Quest(BaseModel):
    id_quest: int | None = None
    name: str
    description: str
    goal: str
    rewards: QuestRewards

class AdventureInfo(BaseModel):
    name: str
    annotation: str = ""
    description_location: str = ""
    description_places: list[str] = []
    location: str
    setting: str
    adventure_image_id: int = -1
    map_image_id: int = -1
    playerNum: int
    npcs: list[NPC] = []
    items: list[Item] = []
    quests: list[Quest] = []


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
