# ============================ Message Template =============================

from worker.text_tasks.schemas import Message, MessageType

# Локация
adventure_info_prompt = Message(
    type=MessageType.user,
    content="""Сгенерируй описание локации для настольной ролевой игры D&D (Dungeons & Dragons) пятой редакции. 
Локация: "{nameLocation}"; жанр: "{nameSetting}"; количество участников: {playerNum}. 
Результат должен быть в формате JSON и содержать объект "location" со следующими ключами: 
"description_location" — название и краткое описание локации (2 предложения); 
"description_places" — массив строк, каждая из которых описывает ключевую точку локации (не более 250 символов)."""
)

adventure_info_answer = Message(
    type=MessageType.assistant,
    content="{description_json_answer}"
)

# Предметы
items_prompt = Message(
    type=MessageType.user,
    content="""Сгенерируй до 4 предметов в формате JSON (по правилам D&D 5-й редакции и в жанре "{nameSetting}"), 
используя описание локации из "description_location". Ответ должен содержать объект "items". 
Каждый предмет должен содержать следующие ключи: 
"name" — название; 
"description" — описание (до 250 символов); 
"values" — стоимость в золоте, серебре или бронзе; 
"type" — тип (оружие, доспехи или сокровища); 
"damage" — урон (только для оружия, в формате XdY, например, 1d8); 
"armor_class" — класс брони (только для доспехов)."""
)

items_answer = Message(
    type=MessageType.assistant,
    content="{items_json_answer}"
)

# NPC
npcs_prompt = Message(
    type=MessageType.user,
    content="""Сгенерируй до 4 NPC в формате JSON (в жанре "{nameSetting}"), основываясь на описании локации ("description_location"). 
Каждый персонаж должен быть связан с одной из ключевых точек из "description_places" (указан её номер в массиве). 
Объект "npc" должен содержать ключи: 
"name" — имя; 
"disc_costum" — описание внешности; 
"role" — роль в локации и указание номера связанной ключевой точки. 
Описание каждого NPC не должно превышать 250 символов."""
)

npcs_answer = Message(
    type=MessageType.assistant,
    content="{characters_json_answer}"
)

# Квесты
quests_prompt = Message(
    type=MessageType.user,
    content="""Сгенерируй не менее {playerNumXthree} квестов в формате JSON, используя информацию о локации, персонажах и предметах. 
Каждый квест должен содержать: 
"name" — название; 
"description" — описание событий, связанных с локацией и NPC (до 250 символов); 
"goal" — цель квеста; 
"rewards" — объект с наградами (ключи: gold, silver, bronze). 
Все квесты должны быть сбалансированы по сложности и наградам."""
)

quests_answer = Message(
    type=MessageType.assistant,
    content="{quests_json_answer}"
)

# Регенирация предметов
items_regeneration_prompt = Message(
    type=MessageType.user,
    content="""Сгенерируй {playerNum} – 4 новых предмета, основанных на описании локации (жанр: "{nameSetting}"). 
Результат должен быть структурирован в объект "items" с ключами: 
"name", "description", "values", "type", "damage" (только для оружия), "armor_class" (только для доспехов). 
Общее описание не должно превышать 500 символов."""
)

items_regeneration_concrete_prompt = Message(
    type=MessageType.user,
    content="""Создай новый предмет вместо "{nameItem}", основываясь на описании локации (жанр: "{nameSetting}"). 
Структурируй результат в объект "items" с ключами: 
"name", "description", "values", "type", "damage" (только для оружия), "armor_class" (только для доспехов). 
Общее описание не должно превышать 500 символов."""
)

# Регенирация NPC
npcs_regeneration_prompt = Message(
    type=MessageType.user,
    content="""Сгенерируй {playerNum} – 4 новых NPC на основе описания локации (жанр: "{nameSetting}"). 
Привяжи их к уже существующим квестам и предметам. 
Объект "npc" должен содержать ключи: 
"name" — имя; 
"disc_costum" — описание внешности; 
"role" — роль в локации. 
Общее описание каждого персонажа не должно превышать 500 символов."""
)

npcs_regeneration_concrete_prompt = Message(
    type=MessageType.user,
    content="""Создай нового NPC вместо "{nameNPC}", используя описание локации (жанр: "{nameSetting}"). 
Учитывай расу, характер и поведение персонажа. Привяжи его к квесту и предметам. 
Объект "npc" должен содержать ключи: 
"name" — имя; 
"disc_costum" — описание внешности; 
"role" — роль в локации. 
Общее описание не должно превышать 500 символов."""
)

# Регенирация квестов
quests_regeneration_prompt = Message(
    type=MessageType.user,
    content="""Сгенерируй {playerNum} – 4 новых квеста на основе описания локации (жанр: "{nameSetting}"). 
Привяжи их к существующим персонажам и предметам. 
Размести квесты в объекте "quests" с ключами: 
"name" — название; 
"description" — описание событий; 
"goal" — цель; 
"rewards" — объект с монетами: gold, silver, bronze. 
Общее содержание ответа не должно превышать 500 символов."""
)

quests_regeneration_concrete_prompt = Message(
    type=MessageType.user,
    content="""Создай новый квест вместо "{name_quest}", используя описание локации (жанр: "{nameSetting}"). 
Используй нового NPC и новые награды. 
Структурируй результат в объект "quests" с ключами: 
"name" — название; 
"description" — описание; 
"goal" — цель; 
"rewards" — объект с монетами: gold, silver, bronze. 
Общее описание не должно превышать 500 символов."""
)
