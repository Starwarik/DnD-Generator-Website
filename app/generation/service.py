from sqlmodel import Session

from app.adventure.models import AdventureState
from app.adventure.service import create_adventure, update_state_content_adventure
from app.adventure.schemas import AdventureInfo
from langchain.schema import HumanMessage, SystemMessage, AIMessage

from app.generation.service_text import text_generation_model

commands = [
    "Для генерации ролевой настольной игры Dungeons & Dragons дано название локации - '{location_name}' в сеттинге '{setting}' с количеством участников – '{num_players}' человека. На основе полученных данных сгенерируй описание локации.",
    "Распиши пункт Предметы: Опиши все возможные сокровища с их числовыми характеристиками не менее 5 штук, которые могут располагаться на территории ранее описанной локации. Описания сокровищ возьми из руководства D&D 5 редакции. Раздели предметы словом '[new]'. После названия предмета обведи ‘[item]’ а в конце описания добавить '[/item]'.",
    "На основе описания Локации, сгенерируй внутриигровых персонажей (их должно быть не менее 8) с именами, кратким описанием для каждого, с учётом: характера, поведения и привяжи каждого из них к квесту для пункта предметы. Раздели персонажей словом '[new]'. После имени персонажа поставь ‘[character]’. И в конце описания персонажа поставить '[/character]'.",
    "На основе сгенерированного описания локации, придумай квесты с подробным описанием (и по возможности - предысторией). Привяжи квесты к ранее описанным персонажам, а также получаемые награды (предметы) из ранее сгенерированных сокровищ. Раздели квесты словом '[new]'. Разделы квестов раздели словом '[section]' а в конце добавить '[/section]'.",
    "На основе сгенерированного описания локации, придумай другой квест и по возможности - предысторией). Привяжи квесты к ранее описанным персонажам,а также получаемые награды (предметы) из ранее сгенерированных сокровищ.",
]


def _generate_iterative_chat(
    instructions: list[str], extra_info: dict[str, str]
) -> list[str]:
    messages = []
    out = []
    for instruction in instructions:
        instruction = instruction.format(**extra_info)
        messages.append(HumanMessage(instruction))
        generated_text = text_generation_model.generate_text(messages)
        messages.append(AIMessage(generated_text))
        out.append(generated_text)
    return out


def generate_adventure_with_models(
    location_name: str,
    setting: str,
    num_players: int,
    user_id: int,
    adventure_id: int,
    session: Session,
):
    """
    extra_info = {'location_name': location_name, 'setting': setting, 'num_players': str(num_players)}
    outputs = _generate_iterative_chat(commands, extra_info=extra_info)
    adventure = update_state_content_adventure(adventure.id, AdventureState.not_ready, AdventureInfo(
        name='Lol', annotation='YA ebal', description='SUKKIN ARKAD', location="asdawsd", setting='adsda', adventure_image_id=1, map_image_id=1, playerNum=1, characters=[], items=[], quests=[]
    ), session)
    """
    pass
