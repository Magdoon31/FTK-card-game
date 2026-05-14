import copy
import random
import pygame

from lib.game_data import load_weapons, load_attacks

# Ensure game data is loaded
load_attacks()
weapons = load_weapons()


class Enemy:


    def __init__(self, name: str, weapon_key: str, max_hp: int = 15):
        self.name = name
        self.effects = {}  # kompatybilne z logiką hero (np. burn)

        self.maxHp = max_hp
        self.hp = self.maxHp

        # Dla kompatybilności z Attack.calculate_damage()
        # (accuracy skaluje po jednej statystyce z attack.accuracy)
        self.stats = {
            "strength": 50,
            "intelligance": 50,
            "talent": 50,
            "focus": 50,
            "speed": 50,
            "luck": 50,
        }

        self.eq = {"weapon": None}
        self.base_defence = 0
        self.base_resistance = 0

        self.eq["weapon"] = weapons[weapon_key]

        # grafika HP paska (boczny ekran)
        self._bar_x = 50
        self._bar_y = 970
        self._bar_w = 250
        self._bar_h = 30

    def res_def(self):
        total_def = self.base_defence
        total_res = self.base_resistance
        if self.effects:
            # hero.py liczy tylko res_up/res_down oraz def_up/def_down
            total_res += sum(1 for e in self.effects if e == "res_up")
            total_res -= sum(1 for e in self.effects if e == "res_down")
            total_def += sum(1 for e in self.effects if e == "def_up")
            total_def -= sum(1 for e in self.effects if e == "def_down")
        return total_res, total_def

    def hurt(self, dmg: int, dmg_type: str) -> bool:
        if dmg_type == "magic":
            dmg -= self.res_def()[0]
            if dmg < 0:
                dmg = 0
            self.hp -= dmg
            if self.hp <= 0:
                self.hp = 0
                return False
            return True

        if dmg_type == "physical":
            dmg -= self.res_def()[1]
            if dmg < 0:
                dmg = 0
            self.hp -= dmg
            if self.hp <= 0:
                return False
            return True

        return True

    def hp_bar(self, screen, title_font):
        fill_width = int(self._bar_w * self.hp / self.maxHp)
        pygame.draw.rect(screen, (255, 0, 0), (self._bar_x, self._bar_y, self._bar_w, self._bar_h))
        pygame.draw.rect(screen, (0, 255, 0), (self._bar_x, self._bar_y, fill_width, self._bar_h))
        screen.blit(title_font.render(f"{self.hp}", True, (200, 255, 240)),(self._bar_x + self._bar_w + 10, self._bar_y - 5),)

    def pick_random_attack(self):
        weapon_obj = self.eq["weapon"]
        idx = random.randrange(0, len(weapon_obj.attacks))
        return idx, weapon_obj.attacks[idx]

    def ai_attack(self, player):

        idx, atk = self.pick_random_attack()
        damage = atk.calculate_damage(self)

        # damage: (final_dmg, successes_list, effect_dict)
        if damage[0] >= 1:
            alive = player.hurt(damage[0], atk.dmg_type)
            pygame.mixer.Sound("assets/sfx/hurt.mp3").play()
        else:
            alive = True

        # efekt (np. burn) — tak jak w main, przepisujemy do effects gracza
        if damage[2] and damage[1].count(False) == 0:
            for effect in damage[2]:
                if effect in ("res_up", "res_down", "def_up", "def_down", "burn"):
                    player.effects[effect] = damage[2][effect]

        return alive

