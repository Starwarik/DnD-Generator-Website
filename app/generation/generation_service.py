from typing import Any
from app.adventure.schemas import *
from app.generation.instructions import *
from app.generation.client_text import TextGenerationModel
from app.generation.schemas import JSONGenerationResult
import json


def parse_json_garbage(s: str) -> dict[str, Any]:
    s = s[next(idx for idx, c in enumerate(s) if c in "{[") :]
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        try:
            return json.loads(s[: e.pos])
        except Exception as e:
            print(s)
            raise e


def generate_text_with_tries(
    instructions: list[TextGenerationInstruction],
    adventure: AdventureInfo,
    model: TextGenerationModel,
    n_tries: int = 3,
) -> AdventureInfo:
    for instruction in instructions:
        prompts = instruction.get_prompts()
        config = instruction.get_config(adventure)
        for i in range(len(prompts)):
            prompts[i].content = prompts[i].content.format(**config)
        generated_result = None
        for _ in range(n_tries):
            try:
                generated_result = model.generate_text(prompts)
            except Exception as e:
                print(_, "try failed")
                print(e)
        if generated_result is None:
            raise Exception("Max tries")
        print("Success")
        generated_json = JSONGenerationResult(
            content=parse_json_garbage(generated_result.content),
            prompt_token_count=generated_result.prompt_token_count,
            assistant_token_count=generated_result.assistant_token_count,
        )
        print(generated_json)
        adventure = instruction.change_adventure_on_success(adventure, generated_json)
    return adventure


def generate_new_adventure(
    location_name: str, setting: str, num_players: int, model: TextGenerationModel
) -> AdventureInfo:
    adventure_info = AdventureInfo(
        name=location_name,
        location=location_name,
        setting=setting,
        playerNum=num_players,
        annotation="",
        description=[],
        characters=[],
        items=[],
        quests=[],
    )

    instructions: list[TextGenerationInstruction] = [
        AdventureInfoInstruction(),
        ItemsInstruction(),
        CharactersInstruction(),
        QuestsInstruction(),
    ]

    return generate_text_with_tries(instructions, adventure_info, model)


def regenerate_new_adventure(
    adventure_info: AdventureInfo, model: TextGenerationModel
) -> AdventureInfo:
    return generate_new_adventure(
        adventure_info.location, adventure_info.setting, adventure_info.playerNum, model
    )


# ============================= QUESTS ========================


def regenerate_quests(
    adventure_info: AdventureInfo, model: TextGenerationModel
) -> AdventureInfo:
    instructions: list[TextGenerationInstruction] = [QuestsRegenerateInstruction()]
    return generate_text_with_tries(instructions, adventure_info, model)


def regenerate_quest_concrete(
    index_quest: int, adventure_info: AdventureInfo, model: TextGenerationModel
) -> AdventureInfo:
    instructions: list[TextGenerationInstruction] = [
        QuestsConcreteRegenerateInstruction(index_quest)
    ]
    return generate_text_with_tries(instructions, adventure_info, model)


# ================================ CHARACTERS ===========================


def regenerate_characters(
    adventure_info: AdventureInfo, model: TextGenerationModel
) -> AdventureInfo:
    instructions: list[TextGenerationInstruction] = [CharactersRegenerateInstruction()]
    return generate_text_with_tries(instructions, adventure_info, model)


def regenerate_character_concrete(
    index_character: int, adventure_info: AdventureInfo, model: TextGenerationModel
) -> AdventureInfo:
    instructions: list[TextGenerationInstruction] = [
        CharactersConcreteRegenerateInstruction(index_character)
    ]
    return generate_text_with_tries(instructions, adventure_info, model)


# ================================== ITEMS ======================================


def regenerate_items(
    adventure_info: AdventureInfo, model: TextGenerationModel
) -> AdventureInfo:
    instructions: list[TextGenerationInstruction] = [ItemsRegenerateInstruction()]
    return generate_text_with_tries(instructions, adventure_info, model)


def regenerate_item_concrete(
    index_item: int, adventure_info: AdventureInfo, model: TextGenerationModel
) -> AdventureInfo:
    instructions: list[TextGenerationInstruction] = [
        ItemsConcreteRegenerateInstruction(index_item)
    ]
    return generate_text_with_tries(instructions, adventure_info, model)
