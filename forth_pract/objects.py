def get_skill_names(skill_keys):
    skill_names = []
    for skill_key in skill_keys:
        skill_data = find_skill_by_key(skill_key)
        if skill_data:
            skill_names.append(skill_data["name"])
    return skill_names


def find_skill_by_key(skill_key):
    if skill_key in skills["learnable"]:
        return skills["learnable"][skill_key]

    # Ищем в уникальных навыках классов
    for class_name in skills["unique"]:
        class_skills = skills["unique"][class_name]
        if skill_key in class_skills:
            return class_skills[skill_key]

    return None


skills = {
    "unique": {
        "peasant": {
            "throw_stone": {
                "name": "Кинуть камень",
                "description": "Наносит 8 урона противнику. Стоимость: 5 маны. Перезарядка: 1 ход.",
                "damage": 8,
                "regeneration": 0,
                "mana_cost": 5,
                "hp_cost": 0,
                "cooldown": 1,
            },
        },
        "speared_peasant": {
            "spear_attack": {
                "name": "Тыкнуть копьем",
                "description": '"Крестьянин с копьем затыкает кого угодно..." Наносит 12 урона противнику. Стоимость: 4 здоровья. Перезарядка: 1 ход',
                "damage": 12,
                "regeneration": 0,
                "mana_cost": 0,
                "hp_cost": 4,
                "cooldown": 1,
            },
        },
        "warrior": {
            "wide_slash": {
                "name": "Широкий горизонтальный разрез",
                "description": "Наносит 18 урона противнику. Стоимость: 12 маны. Перезарядка: 2 хода.",
                "damage": 18,
                "regeneration": 0,
                "mana_cost": 12,
                "hp_cost": 0,
                "cooldown": 2,
            },
            "ram": {
                "name": "Таран",
                "description": "Наносит 25 урона противнику. Стоимость: 8 здоровья. Перезарядка: 3 хода.",
                "damage": 25,
                "regeneration": 0,
                "mana_cost": 0,
                "hp_cost": 8,
                "cooldown": 3,
            },
        },
        "knight": {
            "shove": {
                "name": "Благородный пинок ногой",
                "description": '"С правом данным мне Королем, я пинаю тебя!" Наносит 22 урона противнику. Стоимость: 6 здоровья. Перезарядка: 2 хода.',
                "damage": 22,
                "regeneration": 0,
                "mana_cost": 0,
                "hp_cost": 6,
                "cooldown": 2,
            },
            "catch_breath": {
                "name": "Восстановить дыхание",
                "description": "Восстанавливает 25 здоровья. Стоимость: 20 маны. Перезарядка: 4 хода.",
                "damage": 0,
                "mana_cost": 20,
                "regeneration": 25,
                "hp_cost": 0,
                "cooldown": 4,
            },
        },
        "tank": {
            "shoot": {
                "name": "Выстрел из 125мм пушки",
                "description": "Наносит 45 урона противнику. Стоимость: 15 здоровья. Перезарядка: 4 хода.",
                "damage": 45,
                "mana_cost": 0,
                "regeneration": 0,
                "hp_cost": 15,
                "cooldown": 4,
            },
            "repair": {
                "name": "Ремонтируюсь!",
                "description": "Восстанавливает 35 здоровья. Стоимость: 25 маны. Перезарядка: 5 ходов.",
                "damage": 0,
                "regeneration": 35,
                "armor_bonus": 20,
                "mana_cost": 25,
                "hp_cost": 0,
                "cooldown": 5,
            },
        },
        "heavy": {
            "bonk": {
                "name": "Боньк",
                "description": "Наносит 80 урона противнику. Стоимость: 25 здоровья. Перезарядка: 5 ходов.",
                "damage": 80,
                "mana_cost": 0,
                "hp_cost": 25,
                "cooldown": 5,
            },
            "refresh": {
                "name": "Отдохнуть",
                "description": "Восстанавливает 40 здоровья. Стоимость: 30 маны. Перезарядка: 4 хода.",
                "damage": 0,
                "regeneration": 40,
                "mana_cost": 30,
                "hp_cost": 0,
                "cooldown": 4,
            },
        },
        "achilles": {
            "heel": {
                "name": "Ахилесова Пята",
                "description": "Восстанавливает 50 здоровья. Стоимость: 35 маны. Перезарядка: 6 ходов.",
                "regeneration": 50,
                "damage": 0,
                "mana_cost": 35,
                "hp_cost": 0,
                "cooldown": 6,
            },
        },
        "berserk": {
            "hit_series": {
                "name": "Серия ударов",
                "description": "Что вершит судьбу человечества в этом мире? Наносит 30 урона противнику. Стоимость: 25 маны и 8 здоровья. Перезарядка: 3 хода.",
                "damage": 30,
                "regeneration": 0,
                "mana_cost": 25,
                "hp_cost": 8,
                "cooldown": 3,
            },
            "gun_shoot": {
                "name": "Выстрел из пушки",
                "description": "Некое незримое существо или закон, подобно длани господней, парящей над миром? Наносит 40 урона противнику. Стоимость: 20 здоровья. Перезарядка: 4 хода.",
                "damage": 40,
                "regeneration": 0,
                "mana_cost": 0,
                "hp_cost": 20,
                "cooldown": 4,
            },
            "put_armor": {
                "name": "Надеть шлем берсерка",
                "description": "По крайней мере, истинно то, что человек не властен даже над своей волей. Восстанавливает 45 здоровья. Стоимость: 50 маны. Перезарядка: 7 ходов.",
                "damage": 0,
                "regeneration": 45,
                "armor_bonus": 25,
                "mana_cost": 50,
                "hp_cost": 0,
                "cooldown": 7,
            },
        },
    },
    "learnable": {
        "slash": {
            "name": "Режущий удар",
            "description": "Наносит 15 урона противнику. Стоимость: 8 маны. Перезарядка: 2 хода.",
            "damage": 15,
            "mana_cost": 8,
            "hp_cost": 0,
            "requirements": {"level": 2, "coins": 50},
            "cooldown": 2,
        },
        "fireball": {
            "name": "Огненный шар",
            "description": "Наносит 25 урона противнику. Стоимость: 18 маны. Перезарядка: 3 хода.",
            "damage": 25,
            "mana_cost": 18,
            "hp_cost": 0,
            "requirements": {"level": 3, "coins": 100},
            "cooldown": 3,
        },
        "heal": {
            "name": "Лечение",
            "description": "Восстанавливает 35 здоровья. Стоимость: 30 маны. Перезарядка: 4 хода.",
            "damage": 0,
            "regeneration": 35,
            "mana_cost": 30,
            "hp_cost": 0,
            "requirements": {"level": 4, "coins": 150},
            "cooldown": 4,
        },
    },
    "enemy": {
        "dragon": {
            "first_skill": {
                "name": "Огненное дыхание",
                "description": "хать-пфу, на те в лицо",
                "damage": 35,
                "regeneration": 0,
                "cooldown": 3,
            },
            "second_skill": {
                "name": "Удар хвостом",
                "description": "ХЛОПЬ по роже",
                "damage": 20,
                "regeneration": 10,
                "cooldown": 2,
            },
            "third_skill": {
                "name": "Полет с поджогом земли",
                "description": "Чем воняет? Это кислород, братуха.",
                "damage": 70,
                "regeneration": 0,
                "cooldown": 5,
            },
        },
        "slime": {
            "first_skill": {
                "name": "Плевок слизью",
                "description": "приятного аппетита",
                "damage": 5,
                "regeneration": 3,
                "cooldown": 2,
            },
            "second_skill": {
                "name": "Прыжок",
                "description": "Хоп! И ты в слизи... братик не надо!!!",
                "damage": 8,
                "regeneration": 2,
                "cooldown": 3,
            },
        },
        "goblin": {
            "first_skill": {
                "name": "Удар дубиной",
                "description": "БОНЬК",
                "damage": 12,
                "regeneration": 2,
                "cooldown": 2,
            },
            "second_skill": {
                "name": "Кривая атака",
                "description": "Косоглазие - это семейное!",
                "damage": 15,
                "regeneration": 0,
                "cooldown": 3,
            },
        },
        "skeleton": {
            "first_skill": {
                "name": "Костяная стрела",
                "description": "ЦЕЛЬСЯ! ПЛИ!",
                "damage": 10,
                "regeneration": 3,
                "cooldown": 2,
            },
            "second_skill": {
                "name": "Удар мечом",
                "description": "Тихо украл и ушел, называется я украл твою руку",
                "damage": 14,
                "regeneration": 0,
                "cooldown": 3,
            },
        },
        "master": {
            "first_skill": {
                "name": "Темная магия",
                "description": "Черная магия! Колдун...",
                "damage": 30,
                "regeneration": 15,
                "cooldown": 3,
            },
            "second_skill": {
                "name": "Шлепок",
                "description": "Кажется я зашел не в ту дверь...",
                "damage": 18,
                "regeneration": 8,
                "cooldown": 4,
            },
        },
    },
}
# Словарь с классом игрока/требованием/навыками

roles = {
    "peasant": {
        "name": "Крестьянин",
        "description": "Потерянный в пространстве и времени человек, не знающий, что он делает",
        "min_health": 0,
        "min_power": 0,
        "mana": 20,
        "skills": skills["unique"]["peasant"],
    },
    "speared_peasant": {
        "name": "Крестьянин с копьем",
        "description": "Путь осилит лишь идущий",
        "min_health": 45,
        "min_power": 8,
        "mana": 25,
        "skills": skills["unique"]["speared_peasant"],
    },
    "warrior": {
        "name": "Воин",
        "description": "Интересно, а что будет, если накачать 50 хп и 150 урона?",
        "min_health": 80,
        "min_power": 15,
        "mana": 40,
        "skills": skills["unique"]["warrior"],
    },
    "knight": {
        "name": "Рыцорь",
        "description": "Благородный защитник королевства",
        "min_health": 120,
        "min_power": 20,
        "mana": 60,
        "skills": skills["unique"]["knight"],
    },
    "tank": {
        "name": "T-90M",
        "description": "Стальная мощь на поле боя",
        "min_health": 200,
        "min_power": 25,
        "mana": 80,
        "skills": skills["unique"]["tank"],
    },
    "heavy": {
        "name": "Хэви",
        "description": "палка делает стук стук",
        "min_health": 50,
        "min_power": 150,
        "mana": 70,
        "skills": skills["unique"]["heavy"],
    },
    "achilles": {
        "name": "Ахиллес, сын Пелея",
        "description": "кто ты, воин? ахиллес, сын пелея",
        "min_health": 150,
        "min_power": 28,
        "mana": 90,
        "skills": skills["unique"]["achilles"],
    },
    "swordsman": {
        "name": "Мечник",
        "description": "Передай от меня это послание своему хозяину - черный мечник пришел, так и скажи.",
        "min_health": 110,
        "min_power": 32,
        "mana": 85,
        "skills": skills["unique"]["berserk"],
    },
}
# Словарь с врагами

enemies = {
    "dragon": {
        "name": "дракоша тоша",
        "description": "я не смотрел этот мультик(",
        "health": 300,
        "damage": 30,
        "skills": skills["enemy"]["dragon"],
        "dodge": 5,
        "coins": 500,
    },
    "slime": {
        "name": "Слаймик",
        "description": "до моего прихода в себя тут было что-то интересное",
        "health": 25,
        "damage": 4,
        "skills": skills["enemy"]["slime"],
        "dodge": 15,
        "coins": 25,
    },
    "goblin": {
        "name": "гоблин",
        "description": "хотел сделать голубя, но потом вспомнил, что я уже студент(",
        "health": 50,
        "damage": 8,
        "skills": skills["enemy"]["goblin"],
        "dodge": 10,
        "coins": 40,
    },
    "skeleton": {
        "name": "спуки спуки скелетон",
        "description": "по спине пробегают мурашки",
        "health": 35,
        "damage": 6,
        "skills": skills["enemy"]["skeleton"],
        "dodge": 8,
        "coins": 30,
    },
    "master": {
        "name": "нежить в черной одежде",
        "description": "ох зря я туда полез...",
        "health": 180,
        "damage": 22,
        "skills": skills["enemy"]["master"],
        "dodge": 12,
        "coins": 300,
    },
}

# Словарь с экипировкой

equipment = {
    "weapons": {
        "wooden_sword": {
            "name": "Деревянный меч",
            "description": "великий меч, найденный у подножия великого древа",
            "damage": 5,
            "buy_price": 10,
            "sell_price": 5,
        },
        "iron_sword": {
            "name": "Железный меч",
            "description": "хыщь хыщь, свощь свощь",
            "damage": 15,
            "buy_price": 50,
            "sell_price": 25,
        },
        "dragon_slayer": {
            "name": "Убийца драконов",
            "description": "Я всего лишь хочу быть счастливым",
            "damage": 40,
            "buy_price": 200,
            "sell_price": 100,
        },
    },
    "armors": {
        "leather_armor": {
            "name": "Кожаная броня",
            "description": "Легкая броня из дубленой кожи",
            "defense": 10,
            "buy_price": 30,
            "sell_price": 15,
        },
        "chain_mail": {
            "name": "Кольчуга",
            "description": "Металлические кольца защитят от большинства ударов",
            "defense": 30,
            "buy_price": 80,
            "sell_price": 40,
        },
        "plate_armor": {
            "name": "Латные доспехи",
            "description": "Тяжелая броня, почти как у рыцаря",
            "defense": 50,
            "buy_price": 150,
            "sell_price": 75,
        },
    },
    "potions": {
        "health_potion_small": {
            "name": "Малое зелье здоровья",
            "description": "Восстанавливает немного здоровья",
            "health_restore": 20,
            "mana_restore": 0,
            "buy_price": 15,
            "sell_price": 7,
        },
        "health_potion_large": {
            "name": "Большое зелье здоровья",
            "description": "Восстанавливает много здоровья",
            "health_restore": 50,
            "mana_restore": 0,
            "buy_price": 35,
            "sell_price": 17,
        },
        "mana_potion_small": {
            "name": "Малое зелье маны",
            "description": "Восстанавливает немного маны",
            "health_restore": 0,
            "mana_restore": 25,
            "buy_price": 20,
            "sell_price": 10,
        },
        "mana_potion_large": {
            "name": "Большое зелье маны",
            "description": "Восстанавливает много маны",
            "health_restore": 0,
            "mana_restore": 60,
            "buy_price": 45,
            "sell_price": 22,
        },
        "mixed_potion": {
            "name": "Смешанное зелье",
            "description": "Восстанавливает и здоровье и ману",
            "health_restore": 30,
            "mana_restore": 30,
            "buy_price": 50,
            "sell_price": 25,
        },
    },
}
