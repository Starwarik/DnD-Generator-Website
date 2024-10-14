from typing import Any
from fastapi import BackgroundTasks
from sqlmodel import Session
from app.adventure.schemas import *
from app.generation.instructions import *
from app.generation.service_text import TextGenerationModel
from app.generation.schemas import JSONGenerationResult
import json


class MaxAttemptsExced(Exception):
    pass


def parse_json_garbage(s: str) -> dict[str, Any]:
    s = s[next(idx for idx, c in enumerate(s) if c in "{["):]
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        return json.loads(s[:e.pos])
    

def generate_text_with_tries(instructions: list[TextGenerationInstruction], adventure: AdventureInfo, model: TextGenerationModel, n_tries: int = 3) -> AdventureInfo:
    config: dict[str, str] = {}
    for instruction in instructions:
        prompts = instruction.get_prompts()
        config.update(instruction.get_additional_config(adventure))
        generated_result = None
        for _ in range(n_tries):
            try:
                generated_result = model.generate_text(prompts)
            except Exception:
                pass
        if generated_result is None:
            raise MaxAttemptsExced()
        generated_json = JSONGenerationResult(
            content=parse_json_garbage(generated_result.content),
            prompt_token_count=generated_result.prompt_token_count,
            assistant_token_count=generated_result.assistant_token_count
        )
        adventure = instruction.change_adventure_on_success(adventure, generated_json)
    return adventure

def generate_adventure_with_models(
    location_name: str,
    setting: str,
    num_players: int,
    adventure_id: int,
    background_tasks: BackgroundTasks,
    session: Session,
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
    
    adventure_info = generate_text_with_tries(
        instructions,
        adventure_info,
        model
    )

    adventure = update_state_content_adventure(
        adventure_id,
        AdventureState.image_adventure,
        adventure,
        session
    )

    background_tasks.add_task(
        generate_all_images,
        adventure,
    )