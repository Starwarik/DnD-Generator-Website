from pydantic import BaseModel


class Character(BaseModel):
    name: str
    description: str
    image_id: int | None = None


class Item(BaseModel):
    name: str
    description: str
    image_id: int | None = None


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
    adventure_image_id: int | None = None
    map_image_id: int | None = None
    playerNum: int
    characters: list[Character]
    items: list[Item]
    quests: list[Quest]
