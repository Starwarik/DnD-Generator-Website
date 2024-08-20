from sqlmodel import Session

from app.adventure.models import AdventureState
from app.adventure.service import create_adventure, update_state_content_adventure
from app.adventure.schemas import AdventureInfo, Character, Item, Quest
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from app.generation.prompts import instructions

from app.generation.service_text import text_generation_model

import json

MessageType = HumanMessage | SystemMessage | AIMessage

def _generate_iterative_chat(
    instructions: list[str], extra_info: dict[str, str], previous_chat: list[MessageType] = []
) -> tuple[list[str], list[MessageType]]:
    messages = previous_chat
    out = []
    for instruction in instructions:
        instruction = instruction.format(**extra_info)
        messages.append(HumanMessage(instruction))
        generated_text = text_generation_model.generate_text(messages)
        messages.append(AIMessage(generated_text))
        try:
            out.append(json.loads(generated_text))
        except Exception:
            print(generated_text)
            return out, messages
    return out, messages


def generate_adventure_with_models(
    location_name: str,
    setting: str,
    num_players: int,
    adventure_id: int,
    session: Session,
):
    extra_info = {
        'nameLocation': location_name,
        'nameSetting': setting,
        'playerNum': str(num_players),
        'playerNumXthree': str(num_players * 3)
    }
    out, messages = [], []
    i = 0
    for tries in range(5):
        out_try, messages = _generate_iterative_chat(instructions[i:], extra_info, messages)
        out += out_try
        if len(out) == len(instructions):
            print(out)
            items = [Item(
                name=x['name'],
                description=x['description']
            ) for x in out[1]['items']]
            characters = [Character(
                name=x['name'],
                description=x['description'],
                image_id=-1
            ) for x in out[2]['characters']]
            quests = [Quest(
                name=x['name'],
                description=x['description'],
                goal=x['goal'],
                name_character=x['name_character'],
                name_items=x['name_items'],
            ) for x in out[3]['quests']]
            adventure = AdventureInfo(
                name='/n'.join(list(out[0]['description'].values())),
                annotation='',
                description='',
                location=location_name,
                setting=setting,
                adventure_image_id='',
                map_image_id='',
                playerNum=num_players,
                characters=characters,
                items=items,
                quests=quests
            )
            update_state_content_adventure(
                adventure_id,
                AdventureState.ready,
                adventure,
                session
            )
        else:
            i = len(out)
            messages.pop()
            print(tries, 'try of generation')
    print(messages)
    raise Exception()
