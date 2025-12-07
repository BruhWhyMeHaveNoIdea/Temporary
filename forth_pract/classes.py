from objects import *
from time import sleep
import texts
from functions import get_chance, print_delay
from math import ceil


class Entity:

    def __init__(self):
        self._name = ""
        self._health = 0
        self._power = 0
        self._skills = []
        self._skill_slots = {}
        self.cooldowns = {skill["name"]: 0 for skill in self._skills}  # Исправлено

    def take_damage(self, damage):
        self._health -= damage

    def check_statistic(self):
        s = ""
        s += f"[{self._name}]\n\n"
        s += f"Урон: {self._power};"
        s += f"Здоровье: {self._health};\n"


class Player(Entity):

    def __init__(self):
        super().__init__()
        self._class = "peasant"
        self._name = roles["peasant"]["name"]
        self._health = 20
        self._max_health = 20
        self._mana = 20
        self._max_mana = 20
        self._power = 1
        self._level = 1
        self._inventory = {}
        self._active_equipment = {}
        self._money = 50
        self.cooldowns = {}

    def update_class_skills(self, new_class):

        self._remove_old_class_skills()

        self._add_new_class_skills(new_class)

        self._update_active_skill_slots(new_class)

    def _remove_old_class_skills(self):
        current_skills = self._inventory.get("skills", [])

        class_skill_keys = []
        for class_name in roles.keys():
            class_info = roles[class_name]
            if "skills" in class_info:
                print(class_info["skills"].keys())
                for skill_key in class_info["skills"].keys():
                    class_skill_keys.append(skill_key)

        learned_skills = [
            skill for skill in current_skills if skill not in class_skill_keys
        ]
        self._inventory["skills"] = learned_skills

    def _add_new_class_skills(self, new_class):
        class_info = roles[new_class]
        new_skills = []
        if "skills" in class_info:
            for skill_key in class_info["skills"].keys():
                new_skills.append(skill_key)

        current_skills = self._inventory.get("skills", [])
        for skill in new_skills:
            if skill not in current_skills:
                current_skills.append(skill)

        self._inventory["skills"] = current_skills

    def _update_active_skill_slots(self, new_class):
        class_info = roles[new_class]
        new_skills = []

        if "skills" in class_info:
            new_skills = list(class_info["skills"].keys())

        for slot in ["first", "second", "third"]:
            current_skill = self._active_equipment["skills"][slot]
            if current_skill:
                skill_key = current_skill.get("skill")
                if skill_key and skill_key not in new_skills:
                    self._active_equipment["skills"][slot] = {}

    def increase_health(self, count):
        self._max_health += count
        return texts.health_increased.format(count=count)

    def create_active_inventory(self):
        self._active_equipment = {
            "weapon": {},
            "armor": {},
            "skills": {"first": {}, "second": {}, "third": {}},
            "potions": {
                "first": {},
                "second": {},
                "third": {},
                "forth": {},
                "fifth": {},
            },
        }

        role_skill = skills["unique"][self._class]
        initial_skills = []

        if isinstance(role_skill, dict):
            for skill_key in role_skill.keys():
                initial_skills.append(skill_key)

        self._inventory = {
            "weapons": [],
            "armors": [],
            "potions": {
                "small_hp": 0,
                "small_mana": 0,
                "big_hp": 0,
                "big_mana": 0,
                "mixed": 0,
            },
            "skills": initial_skills,
        }
        return

    def increase_power(self, count):
        self._power += count
        return texts.power_increased.format(count=count)

    def increase_level(self):
        if self._level < 4:
            self._level += 1
            return texts.level_increased.format(level=self._level)
        return texts.max_level

    def change_class(self, new_class: str):
        new_class_lower = new_class.lower()

        class_key = None
        for key in roles.keys():
            if key.lower() == new_class_lower:
                class_key = key
                break

        if class_key is None:
            return texts.class_change_failed

        class_information = roles[class_key]

        health_fits = self._max_health >= class_information["min_health"]
        power_fits = self._power >= class_information["min_power"]

        if health_fits and power_fits:
            old_class = self._name
            new_class_name = class_information[
                "name"
            ]  # Используем имя из информации о классе
            self._name = new_class_name
            self._class = class_key  # Сохраняем ключ класса
            self._max_mana = class_information["mana"]
            self._mana = self._max_mana

            self.update_class_skills(class_key)

            return texts.class_change_success.format(
                old_class=old_class, new_class=new_class_name
            )

        # Этот код теперь не должен выполняться, т.к. проверка в Game
        reason = texts.low_health if not health_fits else texts.low_power
        return texts.class_change_requirements.format(
            reason=reason, health=self._health, power=self._power
        )

    def update_cooldowns(self):
        for skill_name in list(self.cooldowns.keys()):
            if self.cooldowns[skill_name] > 0:
                self.cooldowns[skill_name] -= 1
                if self.cooldowns[skill_name] == 0:
                    del self.cooldowns[skill_name]

    def is_skill_ready(self, skill_name):
        return self.cooldowns.get(skill_name, 0) == 0

    def set_skill_cooldown(self, skill_name, cooldown_duration):
        self.cooldowns[skill_name] = cooldown_duration

    def get_skill_cooldown(self, skill_name):
        return self.cooldowns.get(skill_name, 0)


class EnemyAI:

    def __init__(self, enemy_type, enemy_info):
        self.enemy_type = enemy_type
        self.skills = list(enemy_info.values())
        self.damage = enemies[enemy_type]["damage"]
        self.cooldowns = {skill["name"]: 0 for skill in self.skills}

    def calculate_score(self, skill, enemy_hp, enemy_max_hp, player_hp):
        score = 0

        damage = skill.get("damage", 0)
        if damage > 0:
            kill_bonus = 50 if damage >= player_hp else 0
            score += damage * 2 + kill_bonus

        healing = skill.get("regeneration", 0)
        if healing > 0:
            health_need = 1 - (enemy_hp / enemy_max_hp)
            score += healing * health_need * 3

        cooldown_penalty = skill.get("cooldown", 0) * 5
        score -= cooldown_penalty

        if damage > 0 and healing > 0:
            score += 15

        return score

    def decide_action(self, enemy_hp, enemy_max_hp, player_hp):
        for skill_name in self.cooldowns:
            if self.cooldowns[skill_name] > 0:
                self.cooldowns[skill_name] -= 1

        actions = []

        base_attack = {
            "name": texts.base_attack_name,
            "description": "Враг атакует",
            "damage": self.damage,
            "cooldown": 0,
        }
        base_score = self.calculate_score(
            base_attack, enemy_hp, enemy_max_hp, player_hp
        )
        actions.append((base_score, base_attack))

        for skill in self.skills:
            if self.cooldowns[skill["name"]] == 0:
                score = self.calculate_score(skill, enemy_hp, enemy_max_hp, player_hp)
                actions.append((score, skill))

        best_score, best_action = max(actions, key=lambda x: x[0])

        if best_action["name"] != texts.base_attack_name:
            self.cooldowns[best_action["name"]] = best_action.get("cooldown", 0)

        return best_action


class Game:

    def __init__(self):
        self.player = Player()
        self.days = 7
        self.actions_per_day = 3
        self.left_actions = 3
        self.current_day = 1
        self.game_over = False
        self.ending = None

    def start_game(self):
        print_delay(texts.start_game)
        self.player.create_active_inventory()
        return self.game_loop()

    def game_loop(self):
        while self.current_day <= self.days and not self.game_over:
            if self.left_actions <= 0:
                self.end_day()

            if self.player._money > 1000:
                self.show_ending(3)
                break

            self.show_main_menu()
            try:
                choice = int(input(texts.choose_action))
            except:
                print("Введено не число!")
                continue
            self.process_choice(choice)

    def show_main_menu(self):
        print_delay(
            texts.day_info.format(day=self.current_day, actions=self.left_actions)
        )
        print_delay(texts.main_menu)

    def change_class(self):
        print_delay("=== Смена класса ===")
        print_delay("Доступные классы:")

        class_order = [
            "peasant",
            "speared_peasant",
            "warrior",
            "knight",
            "tank",
            "heavy",
            "achilles",
            "swordsman",
        ]

        for i, class_key in enumerate(class_order, 1):
            class_info = roles[class_key]
            req_health = class_info["min_health"]
            req_power = class_info["min_power"]

            health_ok = self.player._max_health >= req_health
            power_ok = self.player._power >= req_power
            status = "✓" if health_ok and power_ok else "✗"

            print_delay(
                f"{i} - {class_info['name']} [Требуется: {req_health} HP, {req_power} силы] {status}"
            )
            print_delay(f"   {class_info['description']}")
            print_delay(f"   Мана: {class_info['mana']}")
            print_delay("")

        print_delay("0 - Вернуться назад")

        try:
            choice = int(input("Выберите класс: "))
        except ValueError:
            print_delay(texts.invalid_choice)
            return

        if choice == 0:
            return

        if choice < 1 or choice > len(class_order):
            print_delay(texts.invalid_choice)
            return self.change_class()

        selected_class = class_order[choice - 1]
        class_info = roles[selected_class]

        if (
            self.player._max_health >= class_info["min_health"]
            and self.player._power >= class_info["min_power"]
        ):

            old_class = self.player._name
            result = self.player.change_class(selected_class)
            print_delay(result)

            self.player._max_mana = class_info["mana"]
            self.player._mana = self.player._max_mana

            print_delay(texts.new_class_skills)

            if "skills" in class_info:
                for skill_key, skill_info in class_info["skills"].items():
                    print_delay(f"- {skill_info['name']}: {skill_info['description']}")

        else:
            # Показываем, каких характеристик не хватает
            missing = []
            if self.player._max_health < class_info["min_health"]:
                missing.append(
                    f"здоровья (нужно {class_info['min_health']}, у вас {self.player._max_health})"
                )
            if self.player._power < class_info["min_power"]:
                missing.append(
                    f"силы (нужно {class_info['min_power']}, у вас {self.player._power})"
                )

            print_delay(
                texts.class_change_failed_requirements.format(
                    class_name=class_info["name"], missing=", ".join(missing)
                )
            )

        input(texts.press_enter)

    def process_choice(self, choice):
        if choice == 1:
            return self.select_enemy()
        elif choice == 2:
            return self.shop()
        elif choice == 3:
            return self.power_up()
        elif choice == 4:
            return self.show_player_info()
        elif choice == 5:
            return self.change_class()
        else:
            print_delay(texts.invalid_choice)

    def battle(self, enemy):
        enemy_info = enemies[enemy]
        enemy_hp = enemy_info["health"]
        enemy_max_hp = enemy_info["health"]
        enemy_damage = enemy_info["damage"]
        enemy_dodge = enemy_info["dodge"]
        receive_coins = enemy_info["coins"]

        player_max_hp = self.player._max_health
        player_max_mana = self.player._max_mana
        active_inventory = self.player._active_equipment
        damage_reduction = (
            active_inventory["armor"].get("defense", 0) / 100
            if active_inventory.get("armor")
            else 0
        )
        player_damage = (
            active_inventory["weapon"]["damage"] + self.player._power
            if active_inventory["weapon"]
            else self.player._power
        )
        player_skills = active_inventory["skills"]
        escape_chance = 40

        enemy_skills_dict = enemy_info["skills"]  # Это словарь
        enemy_ai = EnemyAI(enemy, enemy_skills_dict)

        move = 1
        print_delay(
            texts.enemy_appears.format(
                enemy_name=enemy_info["name"], description=enemy_info["description"]
            )
        )

        while enemy_hp > 0 and self.player._health > 0:
            print_delay(
                texts.battle_status.format(
                    move=move,
                    enemy_hp=enemy_hp,
                    player_hp=self.player._health,
                    player_mana=self.player._mana,
                )
            )

            self.player.update_cooldowns()

            print_delay(texts.battle_menu)
            while True:
                try:
                    battle_choice = int(input(texts.battle_choice))
                    break
                except:
                    print(texts.invalid_choice)
                    continue

            if battle_choice not in [1, 2, 3, 9]:
                continue

            if battle_choice == 1:
                enemy_dodges = get_chance(enemy_dodge)
                if enemy_dodges:
                    print_delay(texts.attack_missed)
                else:
                    enemy_hp -= player_damage
                    print_delay(texts.attack_success.format(damage=player_damage))
                    if enemy_hp <= 0:
                        break

            elif battle_choice == 2:
                skill_result = self.use_skill()
                if skill_result is None:
                    continue

                skill_name, skill_info = skill_result

                if self.player._mana < skill_info["mana_cost"]:
                    print_delay(texts.not_enough_mana)
                    continue

                if self.player._health <= skill_info["hp_cost"]:
                    print_delay(texts.not_enough_health)
                    continue

                self.player._mana -= skill_info["mana_cost"]
                self.player._health -= skill_info["hp_cost"]

                if skill_info.get("damage", 0) > 0:
                    enemy_dodges = get_chance(enemy_dodge)
                    if enemy_dodges:
                        print_delay(texts.skill_missed)
                    else:
                        damage = skill_info["damage"]
                        enemy_hp -= damage
                        print_delay(
                            texts.skill_damage.format(
                                damage=damage, skill_name=skill_info["name"]
                            )
                        )

                if skill_info.get("regeneration", 0) > 0:
                    heal = skill_info["regeneration"]
                    self.player._health = min(player_max_hp, self.player._health + heal)
                    print_delay(texts.skill_heal.format(heal=heal))

                # Устанавливаем перезарядку
                cooldown = skill_info.get("cooldown", 0)
                if cooldown > 0:
                    self.player.set_skill_cooldown(skill_name, cooldown)
                    print_delay(
                        texts.skill_cooldown.format(
                            skill_name=skill_info["name"], cooldown=cooldown
                        )
                    )

            elif battle_choice == 3:
                potion_result = self.use_potion()
                if not (potion_result):
                    continue

            elif battle_choice == 9:
                escape = get_chance(escape_chance)
                if escape:
                    print_delay(texts.escape_success)
                    self.left_actions -= 1
                    return self.show_main_menu()
                else:
                    print_delay(texts.escape_failed)
                    escape_chance += 5

            if enemy_hp > 0:

                enemy_action = enemy_ai.decide_action(
                    enemy_hp, enemy_max_hp, self.player._health
                )

                print_delay(
                    texts.enemy_action.format(
                        action_name=enemy_action["name"],
                        description=enemy_action["description"],
                    )
                )

                if enemy_action.get("damage", 0) > 0:
                    actual_damage = max(
                        1, ceil(int(enemy_action["damage"] * (1 - damage_reduction)))
                    )
                    self.player._health -= actual_damage
                    print_delay(texts.enemy_damage.format(damage=actual_damage))

                if enemy_action.get("regeneration", 0) > 0:

                    heal_amount = enemy_action["regeneration"]
                    enemy_hp = min(enemy_max_hp, enemy_hp + heal_amount)
                    print_delay(texts.enemy_heal.format(heal=heal_amount))

                move += 1

        if self.player._health <= 0:
            print_delay(texts.battle_lost)
            self.show_ending(1)
        else:
            if enemy == "dragon":
                return self.show_ending(2)
            print_delay(texts.battle_won.format(coins=receive_coins))
            self.player._money += receive_coins
            self.left_actions -= 1
            return

    def select_enemy(self):
        print_delay(texts.enemy_info)
        while True:
            try:
                enemy_choice = int(input(texts.choose_enemy))
                break
            except:
                print(texts.invalid_choice)
        if enemy_choice == 0:
            return

        enemies_dict = {
            1: "slime",
            2: "skeleton",
            3: "goblin",
            4: "master",
            5: "dragon",
        }
        print(enemy_choice)
        try:
            return self.battle(enemies_dict[enemy_choice])
        except:
            print_delay(texts.invalid_enemy)
            return self.select_enemy()

    def use_skill(self):
        from objects import find_skill_by_key

        active_skills = self.player._active_equipment["skills"]

        available_skills = []
        skill_slots = ["first", "second", "third"]

        for i, slot in enumerate(skill_slots, 1):
            skill_data = active_skills[slot]
            if skill_data:
                skill_key = skill_data.get("skill")
                if skill_key:
                    skill_info = find_skill_by_key(skill_key)
                    if skill_info:
                        cooldown = self.player.get_skill_cooldown(skill_key)
                        status = (
                            texts.skill_ready
                            if cooldown == 0
                            else texts.skill_cooldown_info.format(cooldown=cooldown)
                        )
                        available_skills.append(
                            {
                                "slot": i,
                                "name": skill_info["name"],
                                "skill_key": skill_key,
                                "info": skill_info,
                                "status": status,
                            }
                        )

        if not available_skills:
            print_delay(texts.no_skills)
            return None

        print_delay(texts.skills_list)
        for skill in available_skills:
            print_delay(f"{skill['slot']} - {skill['name']}{skill['status']}")
        print_delay(texts.back_option)

        try:
            choice = int(input(texts.choose_skill))
            if choice == 0:
                return None
        except ValueError:
            return None

        selected_skill = None
        for skill in available_skills:
            if skill["slot"] == choice:
                selected_skill = skill
                break

        if not selected_skill:
            print_delay(texts.invalid_skill)
            return None

        if not self.player.is_skill_ready(selected_skill["skill_key"]):
            cooldown_left = self.player.get_skill_cooldown(selected_skill["skill_key"])
            print_delay(texts.skill_not_ready.format(cooldown=cooldown_left))
            return None

        return selected_skill["skill_key"], selected_skill["info"]

    def shop(self):
        print_delay(texts.shop)
        while True:
            try:
                choice = int(input(texts.shop_choice))
                break
            except:
                print(texts.invalid_choice)

        if choice == 0:
            return
        elif choice == 1:
            return self.buy_weapons()
        elif choice == 2:
            return self.buy_armor()
        elif choice == 3:
            return self.buy_potions()
        elif choice == 4:
            return self.buy_skills()
        else:
            print_delay(texts.invalid_shop_choice)
            return self.shop()

    def buy_weapons(self):
        print_delay(texts.weapons)
        while True:
            try:
                weapon_choice = int(input(texts.choose_weapon))
                break
            except:
                print(texts.invalid_choice)

        if weapon_choice == 0:
            return

        weapon_mapping = {
            1: ("wooden_sword", texts.wooden_sword_info),
            2: ("iron_sword", texts.iron_sword_info),
            3: ("dragon_slayer", texts.dragon_slayer_info),
        }

        if weapon_choice in weapon_mapping:
            weapon_key, weapon_text = weapon_mapping[weapon_choice]
            weapon_info = equipment["weapons"][weapon_key]

            print_delay(weapon_text)
            weapon_cost = weapon_info["buy_price"]

            if weapon_key in self.player._inventory["weapons"]:
                print_delay(texts.already_owned_weapon)
                return self.buy_weapons()

            if self.player._money < weapon_cost:
                print_delay(texts.not_enough_money)
                return self.buy_weapons()

            self.player._money -= weapon_cost
            self.player._inventory["weapons"].append(weapon_key)
            print_delay(texts.weapon_purchased)

        return self.buy_weapons()

    def buy_armor(self):
        print_delay(texts.armors)
        while True:
            try:
                armor_choice = int(input(texts.choose_armor))
                break
            except:
                print(texts.invalid_choice)

        if armor_choice == 0:
            return

        armor_mapping = {
            1: ("leather_armor", texts.leather_armor_info),
            2: ("chain_mail", texts.chain_mail_info),
            3: ("plate_armor", texts.plate_armor_info),
        }

        if armor_choice in armor_mapping:
            armor_key, armor_text = armor_mapping[armor_choice]
            armor_info = equipment["armors"][armor_key]

            print_delay(armor_text)
            armor_cost = armor_info["buy_price"]

            if armor_key in self.player._inventory["armors"]:
                print_delay(texts.already_owned_armor)
                return self.buy_armor()

            if self.player._money < armor_cost:
                print_delay(texts.not_enough_money)
                return self.buy_armor()

            self.player._money -= armor_cost
            self.player._inventory["armors"].append(armor_key)
            print_delay(texts.armor_purchased)

        return self.buy_armor()

    def buy_potions(self):
        print_delay(texts.potions)
        while True:
            try:
                potion_choice = int(input(texts.choose_potion))
                break
            except:
                print(texts.invalid_choice)

        if potion_choice == 0:
            return

        potion_mapping = {
            1: ("small_hp", "health_potion_small", texts.small_hp_info),
            2: ("small_mana", "mana_potion_small", texts.small_mana_info),
            3: ("big_hp", "health_potion_large", texts.big_hp_info),
            4: ("big_mana", "mana_potion_large", texts.big_mana_info),
            5: ("mixed", "mixed_potion", texts.mixed_potion_info),
        }

        if potion_choice in potion_mapping:
            inventory_key, equipment_key, potion_text = potion_mapping[potion_choice]
            potion_info = equipment["potions"][equipment_key]

            print_delay(potion_text)
            potion_cost = potion_info["buy_price"]

            if self.player._money < potion_cost:
                print_delay(texts.not_enough_money)
                return self.buy_potions()

            self.player._money -= potion_cost
            self.player._inventory["potions"][inventory_key] += 1
            print_delay(texts.potion_purchased)

        return self.buy_potions()

    def buy_skills(self):
        print_delay(texts.skills_shop)
        while True:
            try:
                skill_choice = int(input(texts.choose_skill_learn))
                break
            except:
                print(texts.invalid_choice)

        if skill_choice == 0:
            return

        skill_mapping = {
            1: ("slash", texts.slash_info),
            2: ("fireball", texts.fireball_info),
            3: ("heal", texts.heal_info),
        }

        if skill_choice in skill_mapping:
            skill_key, skill_text = skill_mapping[skill_choice]
            skill_info = skills["learnable"][skill_key]

            print_delay(skill_text)
            level_required = skill_info["requirements"]["level"]
            coins_required = skill_info["requirements"]["coins"]

            if self.player._level < level_required:
                print_delay(texts.level_too_low)
                return self.buy_skills()

            if self.player._money < coins_required:
                print_delay(texts.not_enough_money)
                return self.buy_skills()

            if skill_key in self.player._inventory["skills"]:
                print_delay(texts.already_known_skill)
                return self.buy_skills()

            self.player._money -= coins_required
            self.player._inventory["skills"].append(skill_key)
            print_delay(texts.skill_learned)

        return self.buy_skills()

    def power_up(self):
        if self.left_actions <= 0:
            return
        print_delay(
            texts.power_up_menu.format(
                health=self.player._health,
                max_health=self.player._max_health,
                mana=self.player._mana,
                max_mana=self.player._max_mana,
                power=self.player._power,
                level=self.player._level,
                money=self.player._money,
            )
        )

        while True:
            try:
                choice = int(input(texts.power_up_choice))
                break
            except:
                print(texts.invalid_choice)

        if choice == 0:
            return

        elif choice == 1:
            cost = 50
            if self.player._money >= cost:
                self.player._money -= cost
                self.player._max_health += 10
                self.player._health = self.player._max_health
                self.player._health = self.player._max_health
                print_delay(texts.health_upgraded.format(value=self.player._max_health))
                self.left_actions -= 1
            else:
                print_delay(texts.not_enough_money)

        elif choice == 2:
            cost = 45
            if self.player._money >= cost:
                self.player._money -= cost
                self.player._power += 10
                print_delay(texts.power_upgraded.format(value=self.player._power))
                self.left_actions -= 1
            else:
                print_delay(texts.not_enough_money)

        elif choice == 3:
            cost = 125
            if self.player._money >= cost:
                if self.player._level < 4:
                    self.player._money -= cost
                    result = self.player.increase_level()
                    print_delay(result)
                    self.left_actions -= 1

                    self.player._max_health += 3
                    self.player._health = self.player._max_health
                    self.player._max_mana += 2
                    self.player._mana = self.player._max_mana
                    self.player._power += 1

                    print_delay(texts.level_up_bonus)
                else:
                    print_delay(texts.max_level)
            else:
                print_delay(texts.not_enough_money)

        elif choice == 4:
            return self.buy_skills()

        else:
            print_delay(texts.invalid_choice)

        sleep(1)
        print_delay(
            texts.stats_updated.format(
                health=self.player._health,
                max_health=self.player._max_health,
                mana=self.player._mana,
                max_mana=self.player._max_mana,
                power=self.player._power,
                level=self.player._level,
                money=self.player._money,
            )
        )

        input(texts.press_enter)
        return self.power_up() if self.left_actions > 0 else self.show_main_menu()

    def show_player_info(self):
        while True:
            print_delay(
                texts.player_info.format(
                    name=self.player._name.capitalize(),
                    health=self.player._health,
                    max_health=self.player._max_health,
                    mana=self.player._mana,
                    max_mana=self.player._max_mana,
                    money=self.player._money,
                    power=self.player._power,
                    level=self.player._level,
                )
            )

            weapon = self.player._active_equipment["weapon"]
            armor = self.player._active_equipment["armor"]
            skills = self.player._active_equipment["skills"]
            potions = self.player._active_equipment["potions"]

            print_delay(
                texts.equipment_status.format(
                    weapon=(
                        weapon.get("name", texts.not_equipped)
                        if weapon
                        else texts.not_equipped
                    ),
                    armor=(
                        armor.get("name", texts.not_equipped)
                        if armor
                        else texts.not_equipped
                    ),
                    skill1=(
                        skills["first"].get("name", texts.not_equipped)
                        if skills["first"]
                        else texts.not_equipped
                    ),
                    skill2=(
                        skills["second"].get("name", texts.not_equipped)
                        if skills["second"]
                        else texts.not_equipped
                    ),
                    skill3=(
                        skills["third"].get("name", texts.not_equipped)
                        if skills["third"]
                        else texts.not_equipped
                    ),
                    potion1=(
                        potions["first"].get("name", texts.not_equipped)
                        if potions["first"]
                        else texts.not_equipped
                    ),
                    potion2=(
                        potions["second"].get("name", texts.not_equipped)
                        if potions["second"]
                        else texts.not_equipped
                    ),
                    potion3=(
                        potions["third"].get("name", texts.not_equipped)
                        if potions["third"]
                        else texts.not_equipped
                    ),
                    potion4=(
                        potions["forth"].get("name", texts.not_equipped)
                        if potions["forth"]
                        else texts.not_equipped
                    ),
                    potion5=(
                        potions["fifth"].get("name", texts.not_equipped)
                        if potions["fifth"]
                        else texts.not_equipped
                    ),
                )
            )

            print_delay(texts.inventory_menu)

            while True:
                try:
                    choice = int(input(texts.inventory_choice))
                    break
                except:
                    print(texts.invalid_choice)

            if choice == 0:
                return
            elif choice == 1:
                self.check_inventory()
            elif choice == 2:
                self.change_active_inventory()
            else:
                print_delay(texts.invalid_choice)

    def check_inventory(self):
        from objects import get_skill_names

        player_inventory = self.player._inventory

        # Получаем названия навыков вместо ключей
        skill_keys = player_inventory["skills"]
        skill_names = get_skill_names(skill_keys)

        print_delay(
            texts.inventory_display.format(
                weapons=(
                    ", ".join(
                        [
                            equipment["weapons"][w]["name"]
                            for w in player_inventory["weapons"]
                        ]
                    )
                    if player_inventory["weapons"]
                    else texts.nothing
                ),
                armors=(
                    ", ".join(
                        [
                            equipment["armors"][a]["name"]
                            for a in player_inventory["armors"]
                        ]
                    )
                    if player_inventory["armors"]
                    else texts.nothing
                ),
                potions=texts.potions_count.format(
                    small_hp=player_inventory["potions"]["small_hp"],
                    small_mana=player_inventory["potions"]["small_mana"],
                    big_hp=player_inventory["potions"]["big_hp"],
                    big_mana=player_inventory["potions"]["big_mana"],
                    mixed=player_inventory["potions"]["mixed"],
                ),
                skills=", ".join(skill_names) if skill_names else texts.nothing,
            )
        )

        input(texts.press_enter)

    def change_active_inventory(self):
        while True:
            print_delay(texts.change_equipment_menu)
            while True:
                try:
                    choice = int(input(texts.equipment_choice))
                    break
                except:
                    print(texts.invalid_choice)

            if choice == 0:
                return
            elif choice == 1:
                self.change_active_weapon()
            elif choice == 2:
                self.change_active_armor()
            elif choice == 3:
                self.change_active_skill()
            elif choice == 4:
                self.change_active_potion()
            else:
                print_delay(texts.invalid_choice)

    def change_active_weapon(self):
        while True:
            player_weapons = self.player._inventory["weapons"]
            if not player_weapons:
                print_delay(texts.no_weapons)
                return

            print_delay(texts.select_weapon)
            for i, weapon_key in enumerate(player_weapons, 1):
                weapon_info = equipment["weapons"][weapon_key]
                print_delay(f"{i} - {weapon_info['name']}")
            print_delay(texts.back_option)

            try:
                while True:
                    try:
                        choice = int(input(texts.choose_weapon_equip))
                        break
                    except:
                        print(texts.invalid_choice)
                if choice == 0:
                    return

                if 1 <= choice <= len(player_weapons):
                    weapon_key = player_weapons[choice - 1]
                    self.player._active_equipment["weapon"] = equipment["weapons"][
                        weapon_key
                    ]
                    print_delay(texts.weapon_equipped)
                else:
                    print_delay(texts.invalid_choice)
            except:
                print_delay(texts.invalid_choice)

    def change_active_armor(self):
        while True:
            player_armors = self.player._inventory["armors"]
            if not player_armors:
                print_delay(texts.no_armor)
                return

            print_delay(texts.select_armor)
            for i, armor_key in enumerate(player_armors, 1):
                armor_info = equipment["armors"][armor_key]
                print_delay(f"{i} - {armor_info['name']}")
            print_delay(texts.back_option)

            try:
                while True:
                    try:
                        choice = int(input(texts.choose_armor_equip))
                        break
                    except:
                        print(texts.invalid_choice)
                if choice == 0:
                    return

                if 1 <= choice <= len(player_armors):
                    armor_key = player_armors[choice - 1]
                    self.player._active_equipment["armor"] = equipment["armors"][
                        armor_key
                    ]
                    print_delay(texts.armor_equipped)
                else:
                    print_delay(texts.invalid_choice)
            except:
                print_delay(texts.invalid_choice)

    def change_active_skill(self):
        while True:
            from objects import get_skill_names, find_skill_by_key

            player_skills = self.player._inventory["skills"]
            if not player_skills:
                print_delay(texts.no_skills_available)
                return  # Выходим в change_active_inventory

            print_delay(texts.select_skill_slot)
            while True:
                try:
                    slot_choice = int(input(texts.choose_slot))
                    break
                except:
                    print(texts.invalid_choice)
            if slot_choice not in [0, 1, 2, 3]:
                print_delay(texts.invalid_slot)
                continue  # Продолжаем цикл, не выходим

            if slot_choice == 0:
                return
            slot_key = ["first", "second", "third"][slot_choice - 1]

            print_delay(texts.select_skill_from_list)

            skill_names = get_skill_names(player_skills)
            for i, skill_name in enumerate(skill_names, 1):
                print_delay(f"{i} - {skill_name}")

            print_delay(texts.back_option)

            try:
                while True:
                    try:
                        skill_choice = int(input(texts.choose_skill_equip))
                        break
                    except:
                        print(texts.invalid_choice)
                if skill_choice == 0:
                    return  # Выходим в change_active_inventory

                if 1 <= skill_choice <= len(player_skills):
                    skill_key = player_skills[skill_choice - 1]
                    skill_info = find_skill_by_key(skill_key)
                    if skill_info:
                        self.player._active_equipment["skills"][slot_key] = {
                            "skill": skill_key,
                            "name": skill_info["name"],
                        }
                        print_delay(texts.skill_equipped)
                    else:
                        print_delay(texts.invalid_choice)
                else:
                    print_delay(texts.invalid_choice)
            except:
                print_delay(texts.invalid_choice)

    def change_active_potion(self):
        while True:
            player_potions = self.player._inventory["potions"]
            available_potions = []

            for potion_type, count in player_potions.items():
                if count > 0:
                    available_potions.append(potion_type)

            if not available_potions:
                print_delay(texts.no_potions)
                return

            print_delay(texts.select_potion_slot)
            while True:
                try:
                    slot_choice = int(input(texts.choose_potion_slot))
                    break
                except:
                    print(texts.invalid_choice)
            if slot_choice not in [0, 1, 2, 3, 4, 5]:
                print_delay(texts.invalid_slot)
                continue

            if slot_choice == 0:
                return

            slot_key = ["first", "second", "third", "forth", "fifth"][slot_choice - 1]

            print_delay(texts.select_potion_from_list)
            potion_mapping = {
                "small_hp": "health_potion_small",
                "small_mana": "mana_potion_small",
                "big_hp": "health_potion_large",
                "big_mana": "mana_potion_large",
                "mixed": "mixed_potion",
            }

            for i, potion_key in enumerate(available_potions, 1):
                potion_name = equipment["potions"][potion_mapping[potion_key]]["name"]
                print_delay(f"{i} - {potion_name} (x{player_potions[potion_key]})")
            print_delay(texts.back_option)

            try:
                while True:
                    try:
                        potion_choice = int(input(texts.choose_potion_equip))
                        break
                    except:
                        print(texts.invalid_choice)
                if potion_choice == 0:
                    return

                if 1 <= potion_choice <= len(available_potions):
                    selected_potion = available_potions[potion_choice - 1]
                    equipment_key = potion_mapping[selected_potion]
                    self.player._active_equipment["potions"][slot_key] = equipment[
                        "potions"
                    ][equipment_key]
                    self.player._inventory["potions"][selected_potion] -= 1
                    print_delay(texts.potion_equipped)
                else:
                    print_delay(texts.invalid_choice)
            except:
                print_delay(texts.invalid_choice)

    def end_day(self):
        self.player._mana = self.player._max_mana
        self.player._health = self.player._max_health
        self.current_day += 1
        self.left_actions = self.actions_per_day
        print_delay(
            texts.new_day.format(day=self.current_day, actions=self.left_actions)
        )

    def use_potion(self):
        print_delay(texts.potion_menu)
        potions = self.player._active_equipment["potions"]

        available_potions = []
        potion_slots = ["first", "second", "third", "forth", "fifth"]

        for i, slot in enumerate(potion_slots, 1):
            potion_data = potions[slot]
            if potion_data:
                potion_name = potion_data["name"]
                available_potions.append(
                    {"slot": i, "name": potion_name, "data": potion_data}
                )
                print_delay(f"{i} - {potion_name}")

        if not available_potions:
            print_delay(texts.no_potions_equipped)
            return False

        print_delay(texts.back_option)

        while True:
            try:
                while True:
                    try:
                        choice = int(input(texts.choose_potion_use))
                        break
                    except:
                        print(texts.invalid_choice)
                if choice == 0:
                    return False
                break
            except ValueError:
                print(texts.invalid_choice)

        selected_potion = None
        for potion in available_potions:
            if potion["slot"] == choice:
                selected_potion = potion
                break

        if not selected_potion:
            print_delay(texts.invalid_choice)
            return False

        potion_info = selected_potion["data"]
        health_restore = potion_info.get("health_restore", 0)
        mana_restore = potion_info.get("mana_restore", 0)

        old_health = self.player._health
        old_mana = self.player._mana

        if health_restore > 0:
            self.player._health = min(
                self.player._max_health, self.player._health + health_restore
            )
            actual_heal = self.player._health
            print_delay(texts.health_restored.format(amount=actual_heal))

        if mana_restore > 0:
            self.player._mana = min(
                self.player._max_mana, self.player._mana + mana_restore
            )
            actual_mana = self.player._mana - old_mana
            print_delay(texts.mana_restored.format(amount=actual_mana))

        slot_key = potion_slots[choice - 1]
        self.player._active_equipment["potions"][slot_key] = {}
        print_delay(texts.potion_used.format(potion_name=potion_info["name"]))
        return True

    def show_ending(self, ending_number: int):
        endings = {1: texts.ending_death, 2: texts.ending_dragon, 3: texts.ending_rich}
        print_delay(endings.get(ending_number, texts.ending_unknown))
        self.game_over = True

    def game_over(self):
        print_delay(texts.game_over_text)
        self.game_over = True
