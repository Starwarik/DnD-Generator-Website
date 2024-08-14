from pydantic import BaseModel


class Character(BaseModel):
    name: str
    description: str
    image_id: int


class Item(BaseModel):
    name: str
    description: str


class Quest(BaseModel):
    name: str
    background: str
    description: str
    reward: str


class AdventureInfo(BaseModel):
    name: str
    annotation: str
    description: str
    location: str
    setting: str
    adventure_image_id: int
    map_image_id: int
    playerNum: int
    characters: list[Character]
    items: list[Item]
    quests: list[Quest]
