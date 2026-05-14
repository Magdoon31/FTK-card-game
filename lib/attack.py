import random


class Attack:
    def __init__(self, name, base_dmg, dmg_type, accuracy, rolls, effect=None,effect_name=None, target_type="single"):
        self.name = name
        self.base_dmg = base_dmg
        self.dmg_type = dmg_type
        self.accuracy = accuracy  # np. {"strength": -10}
        self.rolls = rolls      
        self.effect = effect
        self.effect_name = effect_name
        self.target_type = target_type  # "single", "group"

    def calculate_damage(self,hero):
        successes = []
        
        stat = list(self.accuracy.keys())[0]
        bonus = self.accuracy[stat]
        chance = hero.stats.get(stat, 0) / 100
        for _ in range(self.rolls):
            if random.random() < chance + (bonus/100):
                successes.append(True)
            else:
                successes.append(False)

        dmg = self.base_dmg
        return int(dmg * successes.count(True)//self.rolls), successes, self.effect
