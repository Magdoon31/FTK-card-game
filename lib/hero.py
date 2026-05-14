import copy, pygame
from lib.game_data import load_weapons, load_attacks

load_attacks()
weapons = load_weapons()

class hero:
    def __init__(self, type):
        self.effects = {} #nazwa | długość trwania
        if type.lower() not in ("blacksmith","hunter","scholar","musician"):
            pass
        else:
            self.type = type
            if type == "blacksmith":
                self.maxHp = 15
                self.hp = self.maxHp
                self.stats = {"strength" : 75, "intelligance" : 48, "talent" : 70, "focus" : 52, "speed" : 55, "luck" : 50}
                self.eq = {"weapon" : None, "helmet" : None, "armor" : None, "accessory": None}
                self.base_defence = 1
                self.base_resistance = 1
            elif type == "hunter":
                self.maxHp = 12
                self.hp = self.maxHp
                self.stats = {"strength" : 52, "intelligance" : 65, "talent" : 50, "focus" : 78, "speed" : 76, "luck" : 50}
                self.eq = {"weapon" : None, "helmet" : None, "armor" : None, "accessory": None}
                self.base_defence = 0
                self.base_resistance = 0
            elif type == "scholar":
                self.maxHp = 11
                self.hp = self.maxHp
                self.stats = {"strength" : 48, "intelligance" : 75, "talent" : 52, "focus" : 70, "speed" : 62, "luck" : 50}
                self.eq = {"weapon" : None, "helmet" : None, "armor" : None, "accessory": None}
                self.base_defence = 0
                self.base_resistance = 1
            elif type == "musician":
                self.maxHp = 13
                self.hp = self.maxHp
                self.stats = {"strength" : 65, "intelligance" : 50, "talent" : 78, "focus" : 48, "speed" : 64, "luck" : 60}
                self.eq = {"weapon" : "lute", "helmet" : None, "armor" : None, "accessory": None}
                self.base_defence = 1
                self.base_resistance = 0

    def hurt(self,dmg,dmg_type):

        if dmg_type == "magic":
            dmg -= self.res_def()[0]
            if dmg < 0: dmg = 0
            self.hp -= dmg
            if self.hp <= 0: 
                self.hp = 0
                return False
            return True
        if dmg_type == "physical":
            dmg -= self.res_def()[1]
            if dmg < 0: dmg = 0
            self.hp -= dmg
            if self.hp <= 0: return False
            return True
        
    def hp_bar(self,screen,title):

        bar_width = 250
        bar_height = 30
        fill_width = int(bar_width * self.hp/self.maxHp)
        pygame.draw.rect(screen, (255, 0, 0), (1620, 970, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (1620, 970, fill_width, bar_height))
        screen.blit(title.render(f"{self.hp}",True,(200,255,240)),(1580,965))

    def res_def(self):

        total_def = self.base_defence
        total_res = self.base_resistance
        if self.effects:
            total_res += sum(1 for e in self.effects if e == "res_up")
            total_res -= sum(1 for e in self.effects if e == "res_down")
            total_def += sum(1 for e in self.effects if e == "def_up")
            total_def -= sum(1 for e in self.effects if e == "def_down")

        return total_res, total_def
