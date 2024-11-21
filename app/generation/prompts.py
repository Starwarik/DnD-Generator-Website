# ============================ Message Template =============================

from app.generation.schemas import Message, MessageType


adventure_info_prompt = """Сгенерируй описание локации для ролевой настольной игры Dungeons & Dragons. Локация: "{nameLocation}", жанр: “{nameSetting}и", количество участников: {playerNum}. 
Описание должно быть на русском языке в формате JSON и включать следующие ключи: "name" — название локации; "description_location" - краткое описание локации в двух предложениях; "description_quests" — текстовое описание ключевых точек локации перечислены по номерам.
{
  "name": "Айракс",
  "description_location": "В мире Айракс магия и технологии сосуществуют в гармонии, создавая уникальную атмосферу сказанного фэнтези. Здесь можно встретить как древние руины, так и современные города.",
  "description_quests": [
    "1. В центре города находится древний храм, посвящённый забытому богу. Внутри храма находятся ценные артефакты и свитки с заклинаниями. На полуразрушенных стенах можно увидеть фрески, изображающие сцены из жизни древних обитателей города. Исследуйте храм и найдите скрытые комнаты, чтобы обнаружить древние сокровища.",
    "2. На окраине города расположена заброшенная лаборатория, где проводились эксперименты по созданию големов. Лаборатория охраняется механическими стражами. Некоторые из них всё ещё функционируют и готовы атаковать любого, кто приблизится к лаборатории. Найдите способ отключить механических стражей и исследуйте лабораторию, чтобы найти забытые технологии.",
    "3. За городом находится кладбище, где похоронены жители города. Некоторые из них восстали из мёртвых и превратились в зомби. Зомби бродят по кладбищу в поисках живых. Уничтожьте нежить и восстановите мир на кладбище.",
    "4. В джунглях вокруг города обитают опасные существа, такие как гигантские пауки и ядовитые змеи. Они могут напасть на путников, если те не будут осторожны. Отправляйтесь в джунгли, чтобы собрать редкие ингредиенты для зелий и найти древние руины.",
    "5. В городе также есть несколько жителей, которые готовы помочь искателям приключений. Они расскажут о истории города и подскажут, где искать сокровища. Жители живут в небольших хижинах, разбросанных по городу. Помогите жителям решить их проблемы и получите их поддержку в своих приключениях."
  ]
}"""

adventure_info_answer = "{description_json_answer}"

items_prompt = """Сгенерируй в формате JSON описание возможных сокровищ (не более 4 предметов), которые могут быть найдены на территории ранее описанной локации (объект “location”). Используй описания сокровищ из руководства D&D 5-й редакции. Структурируй результат отдельно в объекте “items”, без включения описания самой локации. Каждый предмет должен содержать ключи: “id_items” – номер предмета; "name" — название предмета; "description" — описание предмета; “values” – Цена предмета в золотых/серебренных/бронзовых, в зависимости на сколько ценен данный предмет, “type” – тип предмета которое может быть: "оружие",  "доспехи",  и "сокровища"; “damage” – урон, который прописан как в Dungeons & Dragons, “armor_class” – класс защиты, который прописан как в Dungeons & Dragons.
{
  "items": [
    {
      "id_items": 1,
      "name": "Амулет защиты",
      "description": "Этот амулет защищает своего владельца от тёмной магии и злых духов.",
      "values": "50 зм",
      "type": "сокровища",
      "damage": null,
      "armor_class": null
    },
    {
      "id_items": 2,
      "name": "Кольцо силы",
      "description": "Это кольцо увеличивает силу своего владельца на 2 пункта.",
      "values": "25 зм",
      "type": "оружие",
      "damage": null,
      "armor_class": null
    },
    {
      "id_items": 3,
      "name": "Щит доблести",
      "description": "Этот щит даёт своему владельцу преимущество на спасброски Харизмы.",
      "values": "75 зм",
      "type": "доспехи",
      "damage": null,
      "armor_class": "+2"
    },
    {
      "id_items": 4,
      "name": "Меч правосудия",
      "description": "Клинок этого меча светится ярким светом, когда его владелец сражается за правое дело.",
      "values": "100 зм",
      "type": "оруществие",
      "damage": "1d8",
      "armor_class": null
    }
  ]
}"""

items_answer = "{items_json_answer}"

characters_prompt = """Сгенерируй в формате JSON описание внутриигровых персонажей (не более 4) для ролевой игры Dungeons & Dragons. Персонажи должны включать: имя, внешность, и их образ жизни. Результат помести в отдельный объект “npc”. Каждый персонаж должен иметь следующие ключи: “id_npc” – номер персонажа; "name" — имя персонажа; “disc_costum” – подробное описание внешности персонажа (до 850 символов);  “dic_life” – описание образа жизни персонажа (до 850 символов).
{
  "npc": [
    {
      "id_npc": 1,
      "name": "Торговец Корвин",
      "disc_costum": "Корвин — крепкий мужчина средних лет с аккуратно подстриженной бородой и усами. Его одежда сшита из дорогих тканей, а на пальцах блестят золотые кольца. Он носит с собой увесистый кошель, полный монет.",
      "dic_life": "Корвин путешествует по миру в поисках выгодных сделок. Он продаёт оружие, доспехи, магические предметы и другие товары, которые могут пригодиться искателям приключений. Корвин всегда готов заключить сделку, но не стоит его обманывать, он может оказаться весьма опасным противником."
    },
    {
      "id_npc": 2,
      "name": "Старейшина Гримбольд",
      "disc_costum": "Гримбольд — седой дварф с длинной бородой и волосами, заплетёнными в косы. Он одет в богато украшенную кольчугу и носит на поясе молот. Гримбольд выглядит мудрым и опытным, его глаза светятся умом.",
      "dic_life": "Гримбольд является старейшиной деревни дварфов. Он заботится о своих соплеменниках и защищает их от врагов. Гримбольд знает много историй о древних битвах и подвигах героев."
    },
    {
      "id_npc": 3,
      "name": "Ведьма Моргана",
      "disc_costum": "Моргана — красивая женщина с длинными чёрными волосами и пронзительными глазами. Она одета в длинное платье, украшенное звёздами и лунами. На шее у неё висит амулет с изображением ворона.",
      "dic_life": "Моргана живёт в лесу недалеко от деревни дварфов. Она изучает магию и общается с духами природы. Жители деревни боятся Моргану и считают её ведьмой."
    },
    {
      "id_npc": 4,
      "name": "Разбойник Кэл",
      "disc_costum": "Кэл — молодой человек с рыжими волосами и веснушками на лице. Он одет в потрёпанную одежду, а на поясе у него висит кинжал. Кэл выглядит хитрым и коварным, его взгляд полон решимости.",
      "dic_life": "Кэл является главарем разбойников, которые грабят путников на дорогах. Он мечтает о богатстве и власти, но пока что вынужден скрываться от стражи."
    }
  ]
}"""

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
