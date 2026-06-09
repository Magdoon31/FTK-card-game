import pytest
from lib.hero import hero
from lib.enemy import Enemy
from lib.game_data import load_attacks, load_weapons

load_attacks()
weapons = load_weapons()

def test_hero_creation():
    player = hero("blacksmith")
    assert player.hp > 0
    assert isinstance(player.stats, dict)

def test_enemy_creation():
    enemy = Enemy("Enemy", weapon_key="bow", max_hp=15)
    assert enemy.hp == 15
    assert enemy.name == "Enemy"

def test_weapon_assignment():
    player = hero("hunter")
    player.eq["weapon"] = weapons["bow"]
    assert player.eq["weapon"].name.lower() == "bow"

def test_damage_calculation():
    player = hero("hunter")
    player.eq["weapon"] = weapons["bow"]

    attack = player.eq["weapon"].attacks[0]
    damage, rolls, effects = attack.calculate_damage(player)

    assert isinstance(damage, (int, float))
    assert isinstance(rolls, list)
    assert len(rolls) == attack.rolls

def test_enemy_takes_damage():
    enemy = Enemy("Enemy", weapon_key="bow", max_hp=15)
    prev_hp = enemy.hp

    alive = enemy.hurt(5, "physical")

    assert enemy.hp < prev_hp
    assert isinstance(alive, bool)

def test_player_takes_damage():
    player = hero("blacksmith")
    prev_hp = player.hp

    alive = player.hurt(5, "physical")

    assert player.hp < prev_hp
    assert isinstance(alive, bool)

    
def test_enemy_death():
    enemy = Enemy("Enemy", weapon_key="bow", max_hp=5)
    alive = enemy.hurt(10, "physical")

    assert alive == False or enemy.hp <= 0
