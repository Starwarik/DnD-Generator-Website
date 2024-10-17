from typing import Any
from fastapi import BackgroundTasks
from sqlmodel import Session
from app.adventure.schemas import *
from app.adventure.service import update_state_content_adventure
from app.generation.instructions import *
from app.generation.service_text import TextGenerationModel
from app.generation.schemas import JSONGenerationResult
import json


def parse_json_garbage(s: str) -> dict[str, Any]:
    s = s[next(idx for idx, c in enumerate(s) if c in "{["):]
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        try:
            return json.loads(s[:e.pos])
        except Exception as e:
            print(s)
            raise e
    
    

def generate_text_with_tries(instructions: list[TextGenerationInstruction], adventure: AdventureInfo, model: TextGenerationModel, n_tries: int = 3) -> AdventureInfo:
    config: dict[str, str] = {}
    for instruction in instructions:
        prompts = instruction.get_prompts()
        config.update(instruction.get_additional_config(adventure))
        for i in range(len(prompts)):
            prompts[i].content = prompts[i].content.format(**config)
        generated_result = None
        for _ in range(n_tries):
            try:
                generated_result = model.generate_text(prompts)
            except Exception as e:
                print(_, 'try failed')
                print(e)
        if generated_result is None:
            raise Exception('Max tries')
        print('Success')
        generated_json = JSONGenerationResult(
            content=parse_json_garbage(generated_result.content),
            prompt_token_count=generated_result.prompt_token_count,
            assistant_token_count=generated_result.assistant_token_count
        )
        print(generated_json)
        adventure = instruction.change_adventure_on_success(adventure, generated_json)
    return adventure

def generate_new_adventure(
    location_name: str,
    setting: str,
    num_players: int,
    model: TextGenerationModel
):
    adventure_info = AdventureInfo(
        name=location_name,
        location=location_name,
        setting=setting,
        playerNum=num_players,
        annotation='',
        description=[],
        characters=[],
        items=[],
        quests=[]
    )

    instructions: list[TextGenerationInstruction] = [
        AdventureInfoInstruction(),
        ItemsInstruction(),
        CharactersInstruction(),
        QuestsInstruction()
    ]
    
    return generate_text_with_tries(
        instructions,
        adventure_info,
        model
    )
