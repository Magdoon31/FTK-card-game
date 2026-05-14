from lib.attack_data import AttackData
from lib.attack import Attack
from lib.weapon import weapon

def load_attacks():
    AttackData.register(Attack(
        name="Heavy Strike",
        base_dmg=5,
        dmg_type="physical",
        accuracy={"strength": 0},
        rolls=2,
        effect="stun",
        effect_name = ["Stun"]
    ))

    AttackData.register(Attack(
        name="Wide Swing",
        base_dmg=3,
        dmg_type="physical",
        accuracy={"strength": 0},
        rolls=3,
        target_type="group"
    ))

    AttackData.register(Attack(
        name="Magic Shot",
        base_dmg=3,
        dmg_type="magic",
        accuracy={"intelligance": 0},
        rolls=1
    ))
    AttackData.register(Attack(
        name="Multi Shot",
        base_dmg=2,
        dmg_type="physical",
        accuracy={"speed": 0},
        target_type="group",
        rolls=3
    ))

    AttackData.register(Attack(
        name="Piercing Arrow",
        base_dmg=4,
        dmg_type="physical",
        accuracy={"focus": 0},
        rolls=2,
    ))

    AttackData.register(Attack(
        name="Fireball",
        base_dmg=3,
        dmg_type="magic",
        accuracy={"intelligance": -10},
        rolls=4,
        target_type="group",
        effect={"burn" : 3},
        effect_name = ["Burn I"]
    ))

    AttackData.register(Attack(
        name="Pizzicato",
        base_dmg=3,
        dmg_type="magic",
        accuracy={"talent": 0},
        rolls=3,
    ))
    AttackData.register(Attack(
        name="Allegretto",
        base_dmg=0,
        dmg_type="magic",
        accuracy={"talent": -5},
        rolls=3,
        target_type="team",
        effect={"speed_up" : 3},
        effect_name = ["Speed Up I"]
    ))

    AttackData.register(Attack(
        name="Harmonic Shield",
        base_dmg=0,
        dmg_type="magic",
        accuracy={"talent": -5},
        rolls=2,
        target_type="you",
        effect={"res_up" : 3},
        effect_name =["Resistance Up I"]
    ))


def load_weapons():
    weapons = {}

    weapons["hammer"] = weapon("Hammer", [
        AttackData.get("Heavy Strike"),
        AttackData.get("Wide Swing")
    ])

    weapons["bow"] = weapon("Bow", [
        AttackData.get("Multi Shot"),
        AttackData.get("Piercing Arrow")
    ])

    weapons["book"] = weapon("Magic Book", [
        AttackData.get("Magic Shot"),
        AttackData.get("Fireball")
    ])

    weapons["lute"] = weapon("Simple Lute", [
        AttackData.get("Pizzicato"),
        AttackData.get("Harmonic Shield")
    ])

    return weapons