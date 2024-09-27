from pydantic import BaseModel


class Character(BaseModel):
    name: str
    description: str
    image_id: int = -1


class Item(BaseModel):
    name: str
    description: str
    image_id: int = -1


class Quest(BaseModel):
    name: str
    description: str
    goal: str
    name_character: str
    name_items: list[str]


class AdventureInfo(BaseModel):
    name: str
    annotation: str
    description: str
    location: str
    setting: str
    adventure_image_id: int = -1
    map_image_id: int = -1
    playerNum: int
    characters: list[Character]
    items: list[Item]
    quests: list[Quest]
