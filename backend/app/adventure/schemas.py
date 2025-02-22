from pydantic import BaseModel


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
    gold: str
    silver: str
    bronze: str

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
