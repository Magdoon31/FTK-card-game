import pygame, random
from lib.hero import hero
from lib.weapon import weapon
from lib.game_data import load_attacks, load_weapons
from lib.enemy import Enemy

load_attacks()
weapons = load_weapons()


pygame.init()
pygame.mixer.init()
pygame.font.init()


enemy = Enemy("Enemy", weapon_key="bow", max_hp=15)

selected_attack = 0

clock = pygame.time.Clock()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
running = True
title = pygame.font.SysFont("arial", 32)
text = pygame.font.SysFont("arial", 22)
attacking_stage = 0
timer = 0
player = hero("blacksmith")


roll_results = []
attack_finished = False
attack_end_time = 0
stats_nr = 0
alive = True
turn = 1
last_turn = 1
whose_turn = "player"
menu = True
selected_hero = 1

sprites = {"false" : pygame.transform.scale(pygame.image.load("assets/image/false_icon.png"),(80,80)),
           "true"  : pygame.transform.scale(pygame.image.load("assets/image/true_icon.png"),(80,80)),
           "defence": pygame.transform.scale(pygame.image.load("assets/image/defence.png"),(55,50)),
           "resistance": pygame.transform.scale(pygame.image.load("assets/image/resistance.png"),(55,50))}
while menu:
    screen.fill((30, 30, 30))
    screen.blit(title.render("Press SPACE to start the battle", True, (255, 255, 255)), (700, 500))

    screen.blit(text.render("1. Blacksmith, Tank", True, (250, 250, 200) if selected_hero == 1 else (200, 200, 200)), (500, 600))
    screen.blit(text.render("2. Hunter, DMG dealer", True, (250, 250, 200) if selected_hero == 2 else (200, 200, 200)), (500, 650))
    screen.blit(text.render("3. Scholar, Magic DMG dealer", True, (250, 250, 200) if selected_hero == 3 else (200, 200, 200)), (500, 700))
    screen.blit(text.render("4. Musician, Support", True, (250, 250, 200) if selected_hero == 4 else (200, 200, 200)), (500, 750))  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu = False
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                menu = False
            if event.key == pygame.K_1:
                selected_hero = 1
            if event.key == pygame.K_2:
                selected_hero = 2
            if event.key == pygame.K_3:
                selected_hero = 3
            if event.key == pygame.K_4:
                selected_hero = 4

    pygame.display.flip()


if selected_hero == 1:
    player = hero("blacksmith")
    player.eq["weapon"] = weapons["hammer"]
elif selected_hero == 2:
    player = hero("hunter")
    player.eq["weapon"] = weapons["bow"]
elif selected_hero == 3:
    player = hero("scholar")
    player.eq["weapon"] = weapons["book"]
elif selected_hero == 4:
    player = hero("musician")
    player.eq["weapon"] = weapons["lute"]


while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 and not attack_finished and attacking_stage ==0:
                selected_attack = 0
            if event.key == pygame.K_2 and not attack_finished and attacking_stage ==0:
                selected_attack = 1
            if event.key == pygame.K_SPACE and not attack_finished and attacking_stage ==0 and whose_turn == "player":
                attacking_stage = 1
                damage = weapon.attacks[selected_attack].calculate_damage(player)

    weapon = player.eq["weapon"]

    for stat in player.stats:
        stats_nr +=1
        screen.blit(text.render(f"|{stat} {player.stats[stat]}|",True,(255,255,255)),(300+stats_nr*160,40))
    stats_nr = 0

    screen.blit(sprites["resistance"],(1600,900))
    screen.blit(title.render(f"{player.res_def()[0]}",True,(255,255,255)),(1620,905))
    screen.blit(sprites["defence"],(1660,900))
    screen.blit(title.render(f"{player.res_def()[1]}",True,(255,255,255)),(1680,905))


    screen.blit(title.render(player.type.capitalize(), True, (255,255,255)), (1740, 900))
    screen.blit(text.render(f"Weapon: {weapon.name}", True, (200,200,200)), (1740, 930))

    screen.blit(text.render("Press SPACE to attack", True, (255,255,255)), (870, 1020))


    if enemy.eq["weapon"]:
        screen.blit(title.render(enemy.name, True, (255, 255, 255)), (50, 900))
        screen.blit(text.render(f"Weapon: {enemy.eq['weapon'].name}", True, (200, 200, 200)), (50, 930))
    enemy.hp_bar(screen, title)



    for i, attack in enumerate(weapon.attacks):
        color = (255,255,0) if i == selected_attack else (255,255,255)

        attack_text = f"{i+1}. {attack.name} (rolls: {attack.rolls})\n max dmg  {attack.base_dmg}"
        if attack.effect:
            for effect in attack.effect_name:
                attack_text += f"\n {effect}"
        screen.blit(text.render(attack_text, True, color), (860, 770 + i*90))
    


    if attacking_stage != 0 and attacking_stage <= weapon.attacks[selected_attack].rolls:
        if timer % 18 == 0:
            roll_results.append(damage[1][attacking_stage-1])

            if roll_results[attacking_stage-1]:
                pygame.mixer.Sound("assets/sfx/success_roll.mp3").play()
            else:
                pygame.mixer.Sound("assets/sfx/missed_roll.mp3").play()

            attacking_stage += 1


    if attacking_stage > weapon.attacks[selected_attack].rolls:
        
        attacking_stage = 0
        attack_finished = True
        attack_end_time = pygame.time.get_ticks()
    if attack_finished:
        if pygame.time.get_ticks() - attack_end_time > 1000:
            timer = timer % 60
            if damage[0] >= 1:
                pygame.mixer.Sound("assets/sfx/hurt.mp3").play()
                enemy_alive = enemy.hurt(damage[0], weapon.attacks[selected_attack].dmg_type)
            else:
                enemy_alive = True

            if damage[2] and roll_results.count(False) == 0:
                for effect in damage[2]:
                    if effect in ("res_up", "res_down", "def_up", "def_down", "burn"):
                        enemy.effects[effect] = damage[2][effect]

            attack_finished = False
            turn += 1
            roll_results = []
            whose_turn = "enemy"

    if enemy.hp <= 0:
        running = False
    elif whose_turn == "enemy" and timer % 60 == 0:
        whose_turn = "player"

        enemy_atk_idx, enemy_atk = enemy.pick_random_attack()
        enemy_damage_raw = enemy_atk.calculate_damage(enemy)
        enemy_current_dmg = enemy_damage_raw[0]
        if enemy_current_dmg >= 1:
            player_alive = player.hurt(enemy_current_dmg, enemy_atk.dmg_type)
            pygame.mixer.Sound("assets/sfx/hurt.mp3").play()
        else:
            player_alive = True

        if enemy_atk and enemy_damage_raw[2] and enemy_roll_results.count(False) == 0:
            for effect in enemy_damage_raw[2]:
                if effect in ("res_up", "res_down", "def_up", "def_down", "burn"):
                    player.effects[effect] = enemy_damage_raw[2][effect]

        if not player_alive:
            running = False


    # efekty statusu po zakończeniu tury gracza+przeciwnika
    if player.effects:
        for effect in list(player.effects.keys()):
            if effect == "burn":
                player.hp -= 1
                pygame.mixer.Sound("assets/sfx/hurt.mp3").play()

            player.effects[effect] -= 1
            if player.effects[effect] <= 0:
                del player.effects[effect]

    if enemy.effects:
        for effect in list(enemy.effects.keys()):
            if effect == "burn":
                enemy.hp -= 1
                pygame.mixer.Sound("assets/sfx/hurt.mp3").play()
                if enemy.hp <= 0:
                    enemy.hp = 0
                    running = False

            enemy.effects[effect] -= 1
            if enemy.effects[effect] <= 0:
                del enemy.effects[effect]

    total_width = weapon.attacks[selected_attack].rolls * 90

    screen_width = screen.get_width()
    start_x = (screen_width - total_width) // 2 

    for j in range(weapon.attacks[selected_attack].rolls):
        pygame.draw.circle(screen,(255,255,255),(start_x+(j+0.5)*90,600),40,5)

    for i, result in enumerate(roll_results):
        
        x = start_x + (i+0.5) * 90

        if result:
            screen.blit(sprites["true"], (x-40, 600-40))
        else:
            screen.blit(sprites["false"], (x-40, 600-40))


    if len(roll_results) != 0:
        per = damage[0] // (weapon.attacks[selected_attack].rolls + 1 - len(roll_results))
        screen.blit(title.render(str(per), True, (210, 90, 40)), (955, 500))

   

    player.hp_bar(screen,title)


    if not alive:
        running = False
        print("You died!")
    timer += 1
    dt = clock.tick(60)
    pygame.display.flip()