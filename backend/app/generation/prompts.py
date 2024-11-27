# ============================ Message Template =============================

from app.generation.schemas import Message, MessageType


adventure_info_prompt = """Сгенерируй описание локации для ролевой настольной игры Dungeons & Dragons. Локация: "{nameLocation}", сеттинг: "{nameSetting}", количество участников: {playerNum}. Описание должно быть на русском языке в формате JSON и включать единственный ключ: "description" — текстовое обобщённое описание локации, в котором ключевые точки локации перечислены по номерам."""

adventure_info_answer = "{description_json_answer}"

items_prompt = """Сгенерируй в формате JSON описание возможных сокровищ (не менее 2 и не более 4), которые могут быть найдены на территории ранее описанной локации (объект “location”). Используй описания сокровищ из руководства D&D 5-й редакции. Структурируй результат отдельно в объекте “items”, без включения описания самой локации. Каждый предмет должен содержать ключи: "name" — название предмета; "description" — описание предмета."""

items_answer = "{items_json_answer}"

characters_prompt = """Сгенерируй в формате JSON описание внутриигровых персонажей (от 2 до 4) для ролевой игры Dungeons & Dragons. Персонажи должны быть привязаны к квесту и локации, их описание должно включать: имя, расу, характер, поведение по отношению к игрокам и роль в квесте. Описание каждого персонажа должно быть представлено одним текстом и содержать не более 750 символов. Результат помести в отдельный объект “players”, как было сделано с объектом “items”. Каждый персонаж должен иметь следующие ключи: "name" — имя персонажа; "description" — обширное текстовое описание персонажа (до 750 символов)."""

characters_answer = "{characters_json_answer}"

quests_prompt = """Сгенерируй не менее 4 квестов, используя информацию из объекта 'location'. В каждом квесте должно быть подробное описание, включающее конкретные события и объекты. Ограничение на описание каждого квеста — не более 850 символов. Структурируй ответ в формате JSON так, чтобы квесты были представлены в объекте “quests”, с ключами: "name" — название квеста; "description" — подробное описание квеста (до 850 символов); "goal" — цель квеста."""

quests_answer = "{quests_json_answer}"

items_regeneration_prompt = """"""

items_regeneration_concrete_prompt = """"""

characters_regeneration_prompt = """"""

characters_regeneration_concrete_prompt = """"""

quests_regeneration_prompt = """"""

quests_regeneration_concrete_prompt = """"""

# ======================================== Template Prompts ======================================================

adventure_info_prompts_messages = [
    Message(type=MessageType.user, content=adventure_info_prompt),
]

items_prompts_messages = adventure_info_prompts_messages + [
    Message(type=MessageType.assistant, content=adventure_info_answer),
    Message(type=MessageType.user, content=items_prompt),
]

characters_prompts_messages = items_prompts_messages + [
    Message(type=MessageType.assistant, content=items_answer),
    Message(type=MessageType.user, content=characters_prompt),
]

quests_prompts_messages = items_prompts_messages + [
    Message(type=MessageType.assistant, content=quests_prompt),
    Message(type=MessageType.user, content=quests_answer),
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

characters_regenerate_prompts_messages = full_context_prompts_messages + [
    Message(type=MessageType.user, content=characters_regeneration_prompt),
]

characters_concrete_regenerate_prompts_messages = full_context_prompts_messages + [
    Message(type=MessageType.user, content=characters_regeneration_concrete_prompt),
]

quests_regenerate_prompts_messages = full_context_prompts_messages + [
    Message(type=MessageType.user, content=quests_regeneration_prompt),
]

quests_concrete_regenerate_prompts_messages = full_context_prompts_messages + [
    Message(type=MessageType.user, content=quests_regeneration_concrete_prompt),
]

# ======================================== Image Prompts =========================================================

character_image_generation = """Нарисуй аватар персонажа по имени: «{char_name}» по описанию: 
{char_description}"""

item_image_generation = """Создай изображение предмета - "{item_name}", соответствующее описанию: 
{item_description}
Изображение должно соответствовать тематике настольной ролевой игры D&D 5 редакции."""

map_image_generation = """Создай карту вид сверху локации {location_name}.
Описание: {location_description}
Карта должна быть создана с учётом особенности настольной ролевой игры D&D 5 редакции.
На изображении не используй текстовые описания, но обозначь цифрами места!"""

adventure_image_generation = """Сгенерируй обложку для ролевой настольной игре Dungeons & Dragons предоставлены данные название приключения: {location_name}. Описание: {location_description}
Обложка (изображение) должна быть в вертикальном формате."""
