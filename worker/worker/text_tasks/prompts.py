# ============================ Message Template =============================

from worker.text_tasks.schemas import Message, MessageType
adventure_info_prompt = """Сгенерируй описание локации для ролевой настольной игры D&D (Dungeons & Dragons) пятой редакции. Локация: "{nameLocation}"; жанр: "{nameSetting}", 
количество участников: {playerNum}. Результат должен быть представлен в формате JSON и включать объект "location" со следующими ключами: 
"description_location" — название локации и краткое описание локации в двух предложениях; 
"description_places" — массив строк, где каждая строка представляет ключевую точку локации, начиная с её номера и содержащая краткое описание (до 250 символов на строку)"""

adventure_info_answer = "{description_json_answer}"

items_prompt = """Сгенерируй в формате JSON описание возможных сокровищ (не более 4 предметов), которые могут быть найдены на территории ранее описанной локации (объект "location"). 
Используй описания сокровищ из руководства D&D пятой редакции и по стилистике должен соответствовать жанру "{nameSetting}". Структурируй результат отдельно в объекте "items", без включения описания самой локации. 
Каждый предмет должен содержать ключи: "name" — название предмета "description" — описание предмета; 
"values" – Цена предмета в золотых/серебренных/бронзовых, в зависимости то на сколько ценен данный предмет, 
"type" – тип предмета с возможными вариантами: "оружие", "доспехи", и "сокровища"; "damage" – урон, в соответствие с кубиками из D&D, "armor_class" – класс защиты, 
который прописан как в D&D. Количество токенов для описания одного сокровища не должно превышать 250 символов"""

items_answer = "{items_json_answer}"

npcs_prompt = """Сгенерируй в формате JSON описание внутриигровых персонажей D&D (не более 4), которые находятся на территории локации, описанной в объекте "location" 
(в соответствии с жанром "{nameSetting}"). 
Персонажи должны быть связаны с описанными местами локации (ключ "description_places") и иметь следующие ключи: "name" — имя персонажа; "disc_costum" — подробное описание внешности персонажа;  
"dic_life" — описание образа жизни и роли персонажа в контексте ключевых мест локации. Свяжи каждого персонажа с одной из ключевых точек локации, используя номер из массива "description_places". 
Результат помести в отдельный объект "npc", без включения описания самой локации. Количество токенов для описания одного персонажа не должно превышать 250 токенов"""

npcs_answer = "{characters_json_answer}"

quests_prompt = """Сгенерируй не менее {playerNumXthree} квестов, используя информацию из объекта "location", а также связанных с персонажами (npc) и сокровищами (items), которые были сгенерированы ранее. 
Каждый квест должен включать: Подробное описание событий, связанных с локацией; Персонажей, участвующих в квесте (npc); Цель квеста; Награды, сбалансированные по сложности квеста  (включающие: Монеты (золото, серебро, бронза); 
Предметы из объекта "items"; Комбинации монет и предметов).
Структурируй ответ в формате JSON так, чтобы квесты были представлены в объекте "quests", с ключами: "name" — название квеста; "description" — подробное описание квеста, включая события, 
персонажей и возможные препятствия; "goal" — цель квеста; "rewards" — объект с наградами, включающий монеты (gold, silver, bronze) и массив предметов из "items". 
Общее количество токенов для описания одного квеста не должно превышать 250"""

quests_answer = "{quests_json_answer}"

items_regeneration_prompt = """Сгенерируй {playerNum} - 4 новых предметов, используя описание локации (в соответствии с жанром "{nameSetting}"). 
Структурируй их в объект "items" с ключами: "name", "description", "values", "type", "damage", "armor_class". Общее содержание ответа не должно привышать 500 символов""""

items_regeneration_concrete_prompt = """Создай новый предмет вместо "{nameItem}", используй описание локации (в соответствии с жанром "{nameSetting}").
Структурируй в объект "items" с ключами: "name", "description", "values", "type", "damage", "armor_class. 
Общее содержание ответа не должно привышать 500 символов""""

npcs_regeneration_prompt = """Сгенерируй {playerNum} - 4 новых персонажей на основе локации (в соответствии с жанром "{nameSetting}"). Привяжи к квестам и предметам. 
Структурируй в объект "npc" с ключами: "name" — имя персонажа; "disc_costum" – подробное описание внешности персонажа; "dic_life" – описание образа жизни персонажа. 
Общее содержание ответа не должно привышать 500 символов"""

npcs_regeneration_concrete_prompt = """Сгенерируй нового персонажа вместо "{nameNPC}" на основе локации, с учётом расы, характера и поведения (в соответствии с жанром "{nameSetting}"). Привяжи к квесту и предметам. 
Структурируй в объект "npc" с ключами: "name" — имя персонажа; "disc_costum" – подробное описание внешности персонажа; "dic_life" – описание образа жизни персонажа. Общее содержание ответа не должно привышать 500 символов"""

quests_regeneration_prompt = """Сгенерируй {playerNum} - 4 новых квестов, используя описание локации (в соответствии с жанром "{nameSetting}"). 
Привяжи их к ранее созданным персонажам и предметам. Помести квесты в объект "quests" с ключами: "name" – название, "description" – описание, "goal" – цель. Общее содержание ответа не должно привышать 500 символов"""

quests_regeneration_concrete_prompt = """Сгенерируй новый квест вместо "{name_quest}", используя описание локации (в соответствии с жанром "{nameSetting}"), с новым персонажем и наградами. 
Помести в объект "quests" с ключами: "name" – название, "description" – описание, "goal" – цель. Общее содержание ответа не должно привышать 500 символов"""


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
