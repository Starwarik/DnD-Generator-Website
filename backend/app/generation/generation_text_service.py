from typing import Any
from app.adventure.schemas import *
from app.generation.instructions import *
from app.generation.text_models import TextGenerationModel
import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.adventure.models import Adventure, AdventureState
from app.adventure.service import create_adventure, update_state_content_adventure


class MaxAttemptsExced(Exception):
    pass


def parse_json_garbage(s: str) -> dict[str, Any]:
    """
    Пытается найти json среди str. Если не получается возращает ошибку JSONDecodeError.
    """
    s = s.replace("'", "\"")
    s = s[next(idx for idx, c in enumerate(s) if c in "{[") :]
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        try:
            return json.loads(s[: e.pos])
        except Exception as e:
            print(s)
            raise e


async def generate_text_with_tries(
    instructions: list[TextGenerationInstruction],
    adventure: AdventureInfo,
    model: TextGenerationModel,
    n_tries: int = 3,
) -> tuple[AdventureInfo, SpentedTokensCounts]:
    """
    Изменение информации приключения по данным инструкциям. На выходе выдает новое приключение.

    :param instructions: Инструкции, по которым будет меняться приключение.
    :param adventure: Изначальное содержание приключения.
    :param model: модель для генрации текста
    :param n_tries: количество попыток генерации перед выбросом ошибки.
    """
    spented_tokens_counts = SpentedTokensCounts()

    for instruction in instructions:
        prompts = instruction.get_prompts()
        config = instruction.get_config(adventure)
        
        for i in range(len(prompts)):
            prompts[i].content = prompts[i].content.format(**config)
        generated_result = None
        for _ in range(n_tries):
            try:
                generated_result = await model.async_generate_text(prompts)
                generated_json: dict[str, Any] = parse_json_garbage(
                    generated_result.content
                )
                print(generated_json)
                adventure = instruction.change_adventure_on_success(
                    adventure, generated_json
                )
            except Exception as e:
                print(_, "try failed")
                print(e)
        if generated_result is None:
            raise MaxAttemptsExced("Max tries")
        print("Success")
        spented_tokens_counts += generated_result.count_tokens
    return (adventure, spented_tokens_counts)


async def generate_new_adventure_json(
    location_name: str,
    setting: str,
    num_players: int,
    model: TextGenerationModel,
    adventure: Adventure,
    session: AsyncSession,
) -> tuple[Adventure, SpentedTokensCounts]:
    """
    Генерирует полноценное приключение с нуля.

    :param location_name: название локации
    :param setting: сеттинг
    :param num_players: кол-во игроков
    :param model: модель для генерации текста
    :param adventure: модель приключения из бд
    :param session: для бд
    """

    adventure_info = AdventureInfo(
        name=location_name,
        location=location_name,
        setting=setting,
        playerNum=num_players,
    )

    instructions: list[TextGenerationInstruction] = [
        AdventureInfoInstruction(),
        ItemsInstruction(),
        NPCsInstruction(),
        QuestsInstruction(),
    ]
    
    adventure_info, spented_tokens_counts = await generate_text_with_tries(
        instructions, adventure_info, model
    )

    adventure = await update_state_content_adventure(
        adventure.id, AdventureState.image_adventure, adventure_info, session
    )
    spented_tokens_counts = SpentedTokensCounts()
    return (adventure, spented_tokens_counts)


async def generate_new_test_adventure_json(
    location_name: str,
    setting: str,
    num_players: int,
    adventure: Adventure,
    session: AsyncSession,
) -> tuple[Adventure, SpentedTokensCounts]:
    """
    Генерирует фиктивное приключение для тестирования.
    :param location_name: название локации
    :param setting: сеттинг
    :param num_players: кол-во игроков
    :param adventure: модель приключения из бд
    :param session: для бд
    """

    dummy_adventure = {
        "name": "Test adventure",
        "annotation": "",
        "description_location": "В мире Айракс магия и технологии сосуществуют в гармонии, создавая уникальную атмосферу сказанного фэнтези. Здесь можно встретить как древние руины, так и современные города.",
        "description_places": [
            "1. В центре города находится древний храм, посвящённый забытому богу. Внутри храма находятся ценные артефакты и свитки с заклинаниями. На полуразрушенных стенах можно увидеть фрески, изображающие сцены из жизни древних обитателей города. Исследуйте храм и найдите скрытые комнаты, чтобы обнаружить древние сокровища.",
            "2. На окраине города расположена заброшенная лаборатория, где проводились эксперименты по созданию големов. Лаборатория охраняется механическими стражами. Некоторые из них всё ещё функционируют и готовы атаковать любого, кто приблизится к лаборатории. Найдите способ отключить механических стражей и исследуйте лабораторию, чтобы найти забытые технологии.",
            "3. За городом находится кладбище, где похоронены жители города. Некоторые из них восстали из мёртвых и превратились в зомби. Зомби бродят по кладбищу в поисках живых. Уничтожьте нежить и восстановите мир на кладбище.",
            "4. В джунглях вокруг города обитают опасные существа, такие как гигантские пауки и ядовитые змеи. Они могут напасть на путников, если те не будут осторожны. Отправляйтесь в джунгли, чтобы собрать редкие ингредиенты для зелий и найти древние руины.",
            "5. В городе также есть несколько жителей, которые готовы помочь искателям приключений. Они расскажут о истории города и подскажут, где искать сокровища. Жители живут в небольших хижинах, разбросанных по городу. Помогите жителям решить их проблемы и получите их поддержку в своих приключениях."
        ],
        "location": location_name,
        "setting": setting,
        "playerNum": num_players,
        "npc": [
            {
                "id_npc": 0,
                "name": "Торговец Корвин",
                "disc_costum": "Корвин — крепкий мужчина средних лет с аккуратно подстриженной бородой и усами. Его одежда сшита из дорогих тканей, а на пальцах блестят золотые кольца. Он носит с собой увесистый кошель, полный монет.",
                "dic_life": "Корвин путешествует по миру в поисках выгодных сделок. Он продаёт оружие, доспехи, магические предметы и другие товары, которые могут пригодиться искателям приключений. Корвин всегда готов заключить сделку, но не стоит его обманывать, он может оказаться весьма опасным противником."
            },
            {
                "id_npc": 1,
                "name": "Старейшина Гримбольд",
                "disc_costum": "Гримбольд — седой дварф с длинной бородой и волосами, заплетёнными в косы. Он одет в богато украшенную кольчугу и носит на поясе молот. Гримбольд выглядит мудрым и опытным, его глаза светятся умом.",
                "dic_life": "Гримбольд является старейшиной деревни дварфов. Он заботится о своих соплеменниках и защищает их от врагов. Гримбольд знает много историй о древних битвах и подвигах героев."
            },
            {
                "id_npc": 2,
                "name": "Ведьма Моргана",
                "disc_costum": "Моргана — красивая женщина с длинными чёрными волосами и пронзительными глазами. Она одета в длинное платье, украшенное звёздами и лунами. На шее у неё висит амулет с изображением ворона.",
                "dic_life": "Моргана живёт в лесу недалеко от деревни дварфов. Она изучает магию и общается с духами природы. Жители деревни боятся Моргану и считают её ведьмой."
            },
            {
                "id_npc": 3,
                "name": "Разбойник Кэл",
                "disc_costum": "Кэл — молодой человек с рыжими волосами и веснушками на лице. Он одет в потрёпанную одежду, а на поясе у него висит кинжал. Кэл выглядит хитрым и коварным, его взгляд полон решимости.",
                "dic_life": "Кэл является главарем разбойников, которые грабят путников на дорогах. Он мечтает о богатстве и власти, но пока что вынужден скрываться от стражи."
            }
        ],
        "items": [
            {
                "id_items": 0,
                "name": "Амулет защиты",
                "description": "Этот амулет защищает своего владельца от тёмной магии и злых духов.",
                "values": "50 зм",
                "type": "сокровища",
                "damage": None,
                "armor_class": None
            },
            {
                "id_items": 1,
                "name": "Кольцо силы",
                "description": "Это кольцо увеличивает силу своего владельца на 2 пункта.",
                "values": "25 зм",
                "type": "оружие",
                "damage": None,
                "armor_class": None
            },
            {
                "id_items": 2,
                "name": "Щит доблести",
                "description": "Этот щит даёт своему владельцу преимущество на спасброски Харизмы.",
                "values": "75 зм",
                "type": "доспехи",
                "damage": None,
                "armor_class": "+2"
            },
            {
                "id_items": 3,
                "name": "Меч правосудия",
                "description": "Клинок этого меча светится ярким светом, когда его владелец сражается за правое дело.",
                "values": "100 зм",
                "type": "оруществие",
                "damage": "1d8",
                "armor_class": None
            }
        ],
        "quests": [
            {
                "id_quest": 0,
                "name": "Test quest 1",
                "description": "Quest Description",
                "goal": "Goal Quest"
            },
            {
                "id_quest": 1,
                "name": "Test quest 2",
                "description": "Quest Description",
                "goal": "Goal Quest"
            },
            {
                "id_quest": 2,
                "name": "Test quest 3",
                "description": "Quest Description",
                "goal": "Goal Quest"
            }
        ],
    }
    spented_tokens_counts = SpentedTokensCounts()
    adventure_info = AdventureInfo.model_validate(dummy_adventure)
    adventure = await update_state_content_adventure(
        adventure.id, AdventureState.image_adventure, adventure_info, session
    )
    return (adventure, spented_tokens_counts)


async def regenerate_new_adventure_json(
    adventure: Adventure, model: TextGenerationModel, session: AsyncSession
) -> tuple[Adventure, SpentedTokensCounts]:
    """
    Перегенерировать всё приключение заново.

    :param adventure: модель приключения из бд
    :param model: модель для генерации текста
    :param session: для бд
    """
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    adventure_info = AdventureInfo(
        name=adventure_info.location,
        location=adventure_info.location,
        setting=adventure_info.setting,
        playerNum=adventure_info.playerNum,
        annotation="",
        description=[],
        npcs=[],
        items=[],
        quests=[],
    )

    instructions: list[TextGenerationInstruction] = [
        AdventureInfoInstruction(),
        ItemsInstruction(),
        CharactersInstruction(),
        QuestsInstruction(),
    ]

    adventure_info, spented_tokens_counts = await generate_text_with_tries(
        instructions, adventure_info, model
    )
    adventure = await update_state_content_adventure(
        adventure.id, AdventureState.image_adventure, adventure_info, session
    )
    return (adventure, spented_tokens_counts)


# ============================= QUESTS ========================


async def regenerate_quests_json(
    adventure: Adventure, model: TextGenerationModel, session: AsyncSession
) -> tuple[Adventure, SpentedTokensCounts]:
    """
    Перегенерировать все квесты заново. Только текстовое содержание.

    :param adventure: модель приключения из бд
    :param model: модель для генерации текста
    :param session: для бд
    """
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    instructions: list[TextGenerationInstruction] = [QuestsRegenerateInstruction()]
    adventure_info, spented_tokens_counts = await generate_text_with_tries(
        instructions, adventure_info, model
    )
    adventure = await update_state_content_adventure(
        adventure.id, AdventureState.ready, adventure_info, session
    )
    return (adventure, spented_tokens_counts)


async def regenerate_quest_concrete_json(
    index_quest: int,
    adventure: Adventure,
    model: TextGenerationModel,
    session: AsyncSession,
) -> tuple[Adventure, SpentedTokensCounts]:
    """
    Перегенерировать конкретный квест заново. Только текстовое содержание.

    :param index_quest: индекс квеста, которого нужно перегенерировать.
    :param adventure: модель приключения из бд
    :param model: модель для генерации текста
    :param session: для бд
    """
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    instructions: list[TextGenerationInstruction] = [
        QuestsConcreteRegenerateInstruction(index_quest)
    ]
    adventure_info, spented_tokens_counts = await generate_text_with_tries(
        instructions, adventure_info, model
    )
    adventure = await update_state_content_adventure(
        adventure.id, AdventureState.ready, adventure_info, session
    )
    return (adventure, spented_tokens_counts)


# ================================ NPCS ===========================


async def regenerate_characters_json(
    adventure: Adventure, model: TextGenerationModel, session: AsyncSession
) -> tuple[Adventure, SpentedTokensCounts]:
    """
    Перегенерировать всех персонажей заново. Только текстовое содержание.

    :param adventure: модель приключения из бд
    :param model: модель для генерации текста
    :param session: для бд
    """
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    instructions: list[TextGenerationInstruction] = [NPCsRegenerateInstruction()]
    adventure_info, spented_tokens_counts = await generate_text_with_tries(
        instructions, adventure_info, model
    )
    adventure = await update_state_content_adventure(
        adventure.id, AdventureState.image_characters, adventure_info, session
    )
    return (adventure, spented_tokens_counts)


async def regenerate_character_concrete_json(
    index_character: int,
    adventure: Adventure,
    model: TextGenerationModel,
    session: AsyncSession,
) -> tuple[Adventure, SpentedTokensCounts]:
    """
    Перегенерировать конкретный персонажа заново. Только текстовое содержание.

    :param index_character: индекс персонажа, которого нужно перегенерировать.
    :param adventure: модель приключения из бд
    :param model: модель для генерации текста
    :param session: для бд
    """
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    instructions: list[TextGenerationInstruction] = [
        NPCsConcreteRegenerateInstruction(index_character)
    ]
    adventure_info, spented_tokens_counts = await generate_text_with_tries(
        instructions, adventure_info, model
    )
    adventure = await update_state_content_adventure(
        adventure.id, AdventureState.image_characters, adventure_info, session
    )
    return (adventure, spented_tokens_counts)


# ================================== ITEMS ======================================


async def regenerate_items_json(
    adventure: Adventure, model: TextGenerationModel, session: AsyncSession
) -> tuple[Adventure, SpentedTokensCounts]:
    """
    Перегенерировать все предметы заново. Только текстовое содержание.

    :param adventure: модель приключения из бд
    :param model: модель для генерации текста
    :param session: для бд
    """
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    instructions: list[TextGenerationInstruction] = [ItemsRegenerateInstruction()]
    adventure_info, spented_tokens_counts = await generate_text_with_tries(
        instructions, adventure_info, model
    )
    adventure = await update_state_content_adventure(
        adventure.id, AdventureState.image_items, adventure_info, session
    )
    return (adventure, spented_tokens_counts)


async def regenerate_item_concrete_json(
    index_item: int,
    adventure: Adventure,
    model: TextGenerationModel,
    session: AsyncSession,
) -> tuple[Adventure, SpentedTokensCounts]:
    """
    Перегенерировать конкретный предмет заново. Только текстовое содержание.

    :param index_item: индекс предмет, которого нужно перегенерировать.
    :param adventure: модель приключения из бд
    :param model: модель для генерации текста
    :param session: для бд
    """
    adventure_info = AdventureInfo.model_validate_json(adventure.content)
    instructions: list[TextGenerationInstruction] = [
        ItemsConcreteRegenerateInstruction(index_item)
    ]
    adventure_info, spented_tokens_counts = await enerate_text_with_tries(
        instructions, adventure_info, model
    )
    adventure = await update_state_content_adventure(
        adventure.id, AdventureState.image_items, adventure_info, session
    )
    return (adventure, spented_tokens_counts)
