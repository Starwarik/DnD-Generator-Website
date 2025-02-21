# ============================ Message Template =============================

from worker.text_tasks.schemas import Message, MessageType

adventure_info_prompt = """Сгенерируй описание локации для настольной ролевой игры D&D (Dungeons & Dragons) пятой редакции. Локация: "{nameLocation}"; жанр: "{nameSetting}"; количество участников: {playerNum}. Результат должен быть в формате JSON и содержать объект "location" с ключами: "description_location" — название и краткое описание локации (2 предложения); "description_places" — массив строк, каждая строка описывает ключевую точку локации (не более 250 символов)."""

adventure_info_answer = "{description_json_answer}"

items_prompt = """Сгенерируй в формате JSON до 4 сокровищ (по правилам D&D 5-e редации, и с учетом жанра "{nameSetting}"), описания локации которой, храниться в "description_location". Ответ должен содержать объект "items", без описания локации. Каждый предмет включает ключи: "name" — название; "description" — описание (до 250 символов); "values" — стоимость в золоте, серебре или бронзе; "type" — оружие, доспехи или сокровища; "damage" — урон (только для оружия); "armor_class" — класс брони (только для доспехов)."""

items_answer = "{items_json_answer}"

npcs_prompt = """Сгенерируй до 4 NPC в формате JSON (по жанру "{nameSetting}"), описания локации которой, храниться в "description_location". Персонажи должны быть связаны с ключевыми точками из "description_places". Объект "npc" содержит: "name" — имя; "disc_costum" — описание внешности; "dic_life" — роль в локации, связанная с одной из точек (указан её номер). Описание каждого NPC не должно превышать 250 символов."""

npcs_answer = "{characters_json_answer}"

quests_prompt = """Сгенерируй не менее {playerNumXthree} квестов в формате JSON, используя "location", "npc" и "items". Каждый квест включает: "name" — название; "description" — события, связанные с локацией и персонажами (до 250 символов); "goal" — цель квеста; "rewards" — объект с наградами (монеты: gold, silver, bronze и предметы из "items"). Все квесты должны быть сбалансированы по сложности и наградам."""

quests_answer = "{quests_json_answer}"

items_regeneration_prompt = """Сгенерируй {playerNum} - 4 новых предмета по описанию локации (жанр "{nameSetting}"). Структурируй в объект "items" с ключами: "name", "description", "values", "type", "damage" (только для оружия), "armor_class" (только для брони). Общее описание не должно превышать 500 символов"""

items_regeneration_concrete_prompt = """Создай новый предмет вместо "{nameItem}", используя описание локации (жанр "{nameSetting}"). Структурируй в объект "items" с ключами: "name", "description", "values", "type", "damage" (только для оружия), "armor_class" (только для брони). Общее описание не должно превышать 500 символов"""

npcs_regeneration_prompt = """Сгенерируй {playerNum} - 4 новых NPC на основе локации (жанр "{nameSetting}"). Привяжи их к квестам и предметам. Объект "npc" содержит ключи: "name" — имя; "disc_costum" — описание внешности; "dic_life" — образ жизни и роль. Общее описание не должно превышать 500 символов"""

npcs_regeneration_concrete_prompt = """Сгенерируй нового NPC вместо "{nameNPC}" на основе локации (жанр "{nameSetting}"). Учти расу, характер и поведение. Привяжи его к квесту и предметам. Объект "npc" содержит ключи: "name" — имя; "disc_costum" — описание внешности; "dic_life" — образ жизни. Общее описание не должно превышать 500 символов"""

quests_regeneration_prompt = """Сгенерируй {playerNum} - 4 новых квеста, используя описание локации (жанр "{nameSetting}"). Привяжи их к ранее созданным NPC и предметам. Объект "quests" включает: "name" — название; "description" — события; "goal" — цель. Общее описание не должно превышать 500 символов"""

quests_regeneration_concrete_prompt = """Сгенерируй новый квест вместо "{name_quest}", используя описание локации (жанр "{nameSetting}"), нового персонажа и награды. Объект "quests" включает ключи: "name" — название; "description" — события; "goal" — цель. Общее описание не должно превышать 500 символов"""


# ======================================== Template Prompts ======================================================

adventure_info_prompts_messages = [
    Message(type=MessageType.user, content=adventure_info_prompt),
]

items_prompts_messages = adventure_info_prompts_messages + [
    Message(type=MessageType.assistant, content=adventure_info_answer),
    Message(type=MessageType.user, content=items_prompt),
]

npcs_prompts_messages = items_prompts_messages + [
    Message(type=MessageType.assistant, content=items_answer),
    Message(type=MessageType.user, content=npcs_prompt),
]

quests_prompts_messages = items_prompts_messages + [
    Message(type=MessageType.assistant, content=npcs_answer),
    Message(type=MessageType.user, content=quests_prompt),
]

full_context_prompts_messages = quests_prompts_messages + [
    Message(type=MessageType.assistant, content=quests_answer),
]

items_regenerate_prompts_messages = full_context_prompts_messages + [
    Message(type=MessageType.user, content=items_regeneration_prompt),
]

items_concrete_regenerate_prompts_messages = full_context_prompts_messages + [
    Message(type=MessageType.user, content=items_regeneration_concrete_prompt),
]

npcs_regenerate_prompts_messages = full_context_prompts_messages + [
    Message(type=MessageType.user, content=npcs_regeneration_prompt),
]

npcs_concrete_regenerate_prompts_messages = full_context_prompts_messages + [
    Message(type=MessageType.user, content=npcs_regeneration_concrete_prompt),
]

quests_regenerate_prompts_messages = full_context_prompts_messages + [
    Message(type=MessageType.user, content=quests_regeneration_prompt),
]

quests_concrete_regenerate_prompts_messages = full_context_prompts_messages + [
    Message(type=MessageType.user, content=quests_regeneration_concrete_prompt),
]
