from abc import ABC, abstractmethod

import app.generation.prompts as prompts_template

from typing import final

import json

from app.adventure.schemas import *
from app.generation.schemas import *

class TextGenerationInstruction(ABC):
    @abstractmethod
    def get_prompts(self) -> list[Message]:
        raise NotImplementedError()

    @abstractmethod
    def get_additional_config(self, adventure: AdventureInfo) -> dict[str, str]:
        raise NotImplementedError()
    
    @abstractmethod
    def change_adventure_on_success(self, adventure: AdventureInfo, result: JSONGenerationResult) -> AdventureInfo:
        raise NotImplementedError()

    
@final
class AdventureInfoInstruction(TextGenerationInstruction):
    def get_prompts(self) -> list[Message]:
        return [
            Message(
                type = MessageType.system,
                content = prompts_template.instruction_system
            ),
            Message(
                type = MessageType.user,
                content = prompts_template.generate_prompt
            )
        ]

    def get_additional_config(self, adventure: AdventureInfo) -> dict[str, str]:
        return {
            'nameLocation': adventure.location,
            'nameSetting': adventure.setting,
            'playerNum': str(adventure.playerNum),
            'playerNumXthree': str(adventure.playerNum*3)
        }
    
    def change_adventure_on_success(self, adventure: AdventureInfo, result: JSONGenerationResult) -> AdventureInfo:
        generated_answer = AdventureInfoInstructionAnswer.model_validate(result.content)
        generated_description = generated_answer.description
        if type(generated_description) is str:
            adventure.description = generated_description.split('/n')
        elif type(generated_description) is list:
            adventure.description = generated_description
        elif type(generated_description) is dict:
            adventure.description = list(generated_description.values())
        return adventure

@final
class ItemsInstruction(TextGenerationInstruction):
    def get_prompts(self) -> list[Message]:
        return [
            Message(
                type=MessageType.system,
                content=prompts_template.instruction_system
            ),
            Message(
                type=MessageType.user,
                content=prompts_template.generate_prompt
            ),
            Message(
                type=MessageType.assistant,
                content=prompts_template.generate_answer
            ),
            Message(
                type=MessageType.user,
                content=prompts_template.items_prompt
            )
        ]

    def get_additional_config(self, adventure: AdventureInfo) -> dict[str, str]:
        description = {(i+1):x for i, x in enumerate(adventure.description)}
        return {
            'description_json_answer': json.dumps(description, indent=4)
        }
    
    def change_adventure_on_success(self, adventure: AdventureInfo, result: JSONGenerationResult) -> AdventureInfo:
        generated_answer = ItemInstructionAnswer.model_validate(result.content)
        adventure.items = [
            Item(
                name=x.name,
                description=x.description
            ) for x in generated_answer.items
        ]
        return adventure


@final
class CharactersInstruction(TextGenerationInstruction):
    def get_prompts(self) -> list[Message]:
        return [
            Message(
                type=MessageType.system,
                content=prompts_template.instruction_system
            ),
            Message(
                type=MessageType.user,
                content=prompts_template.generate_prompt
            ),
            Message(
                type=MessageType.assistant,
                content=prompts_template.generate_answer
            ),
            Message(
                type=MessageType.user,
                content=prompts_template.items_prompt
            ),
            Message(
                type=MessageType.assistant,
                content=prompts_template.items_answer
            ),
            Message(
                type=MessageType.user,
                content=prompts_template.characters_prompt
            )
        ]

    def get_additional_config(self, adventure: AdventureInfo) -> dict[str, str]:
        items = {
            'items':[
                {
                    'name': x.name,
                    'description': x.description
                } for x in adventure.items
            ]
        }
        return {
            'items_json_answer': json.dumps(items, indent=4)
        }
    
    def change_adventure_on_success(self, adventure: AdventureInfo, result: JSONGenerationResult) -> AdventureInfo:
        generated_answer = CharactersInstructionAnswer.model_validate(result.content)
        adventure.characters = [
            Character(
                name=x.name,
                description=x.description
            ) for x in generated_answer.players
        ]
        return adventure

@final
class QuestsInstruction(TextGenerationInstruction):
    def get_prompts(self) -> list[Message]:
        return [
            Message(
                type=MessageType.system,
                content=prompts_template.instruction_system
            ),
            Message(
                type=MessageType.user,
                content=prompts_template.generate_prompt
            ),
            Message(
                type=MessageType.assistant,
                content=prompts_template.generate_answer
            ),
            Message(
                type=MessageType.user,
                content=prompts_template.items_prompt
            ),
            Message(
                type=MessageType.assistant,
                content=prompts_template.items_answer
            ),
            Message(
                type=MessageType.user,
                content=prompts_template.characters_prompt
            ),
            Message(
                type=MessageType.assistant,
                content=prompts_template.characters_answer
            ),
            Message(
                type=MessageType.user,
                content=prompts_template.quest_prompt
            )
        ]

    def get_additional_config(self, adventure: AdventureInfo) -> dict[str, str]:
        characters = {
            'players': [
                {
                    'name': x.name,
                    'description': x.description
                } for x in adventure.characters
            ]
        }
        return {
            'characters_json_answer': json.dumps(characters, indent=4)
        }
    
    def change_adventure_on_success(self, adventure: AdventureInfo, result: JSONGenerationResult) -> AdventureInfo:
        generated_answer = QuestsInstructionAnswer.model_validate(result.content)
        adventure.quests = [
            Quest(
                name=x.name,
                description=x.description,
                goal=x.goal
            ) for x in generated_answer.quests
        ]
        return adventure