from pydantic import BaseModel


class Character(BaseModel):
    id_npc: str
    name: str
    disc_costum: str
    dic_life: str
    image_id: int = -1


class Item(BaseModel):
    id_items: int
    name: str
    description: str
    values: str
    type: str
    damage: str | None
    armor_class: str | None
    image_id: int = -1


class Quest(BaseModel):
    name: str
    description: str
    goal: str


class AdventureInfo(BaseModel):
    annotation: str = ""
    location: str
    setting: str
    playerNum: int

    name: str
    description_location: str = ""
    description_quests: list[str] = []

    adventure_image_id: int = -1
    map_image_id: int = -1

    characters: list[Character] = []
    items: list[Item] = []
    quests: list[Quest] = []
