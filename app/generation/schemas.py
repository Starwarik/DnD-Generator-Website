from pydantic import BaseModel


class GenerationAnswer(BaseModel):
    name: str
    setting: str
    description: dict[str, str]

class ItemAnswer(BaseModel):
    name: str
    

class ItemsAnswer(BaseModel):
    name: str
    setting: str
    description: Dict[str, str]