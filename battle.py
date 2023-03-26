import pygame
import random
from pygame.locals import *

from bar import view_enemy_score
from text import view_text

WHITE = (255, 255, 255)

# imgBtlBG = pygame.image.load("image/btlbg.png")


ENEMY_NAME_LIST = [
    "Buggy", "Arlong", "Sir Crocodile", "Eneru", "Rob Lucci",
    "Gecko Moria", "Admiral of the Navye", "Doflamingo", "Big Mom&Kaido", "Marshall D. Teach"
]

ENEMY_SKILL_LIST = [
    "Special Buggy Gun", "Shark, ON, Tooth", "Desert Raspada", "200 million V Thunder God", "Maximum ring six king gun",
    "Shadows Asgard", "Inugami Guren", "god thread", "Raimei Hakkake", "Black Hole"
]

COMMAND = ["[A]ttack", "[C]hopper Cure", "[H]lep Shipmate", "[R]un"]
BLINK = [
    (224, 255, 255),
    (192, 240, 255),
    (128, 224, 255),
    (64, 192, 255),
    (128, 224, 255),
    (192, 240, 255)
]


# initiate battle
def init_battle(
    floor: int,
):
    typ = random.randint(0, floor)
    # the number enemy is 10, 0~9
    if floor >= 10:
        typ = random.randint(0, 9)
    lev = random.randint(1, floor)
    img_enemy = pygame.image.load("image/character/enemy" + str(typ) + ".png")
    enemy_name = ENEMY_NAME_LIST[typ] + " LV" + str(lev)
    enemy_skill = ENEMY_SKILL_LIST[typ]
    enemy_life_max = 60 * (typ + 1) + (lev - 1) * 10
    enemy_life = enemy_life_max
    enemy_str = int(enemy_life_max / 8)
    enemy_x = 440 - img_enemy.get_width() / 2
    enemy_y = 560 - img_enemy.get_height()

    return (
        img_enemy, enemy_name, enemy_skill,
        enemy_life_max, enemy_life, enemy_str,
        enemy_x, enemy_y,
    )


# view battle
def view_battle(
    screen, fnt, message, imgBack,
    imgEnemy, enemy_life, enemy_life_max, enemy_x, enemy_y, enemy_step, enemy_blink,
    dmg_eff,
):
    bx = 0
    by = 0
    # screen shaking
    if dmg_eff > 0:
        dmg_eff = dmg_eff - 1
        bx = random.randint(-20, 20)
        by = random.randint(-10, 10)
    screen.blit(imgBack, [bx, by])

    # enemy damage flash
    if enemy_life > 0 and enemy_blink % 2 == 0:
        screen.blit(imgEnemy, [enemy_x, enemy_y + enemy_step])

    # view enemy score
    view_enemy_score(screen, 340, 580, 200, 10, enemy_life, enemy_life_max)
    # enemy damage flash period
    if enemy_blink > 0:
        enemy_blink = enemy_blink - 1

    # view message
    for i in range(10):
        view_text(screen, message[i], 600, 100 + i * 50, fnt, WHITE)

    return dmg_eff, enemy_blink


# battle command input
def battle_command(
    screen, fnt, key,
    btl_cmd,
    tmr
):
    ent = False
    # push a button, attack
    if key[K_a]:
        btl_cmd = 0
        ent = True
    # push c button, chopper cure
    if key[K_c]:
        btl_cmd = 1
        ent = True
    # push h button, help shipment
    if key[K_h]:
        btl_cmd = 2
        ent = True
    # push r button, run
    if key[K_r]:
        btl_cmd = 3
        ent = True
    # push r button, run
    if key[K_UP] and btl_cmd > 0:  # ↑キー
        btl_cmd -= 1
    # push r button, run
    if key[K_DOWN] and btl_cmd < 3:  # ↓キー
        btl_cmd += 1
    if key[K_SPACE] or key[K_RETURN]:
        ent = True
    for i in range(4):
        colour = WHITE
        if btl_cmd == i:
            colour = BLINK[tmr % 6]
        view_text(screen, COMMAND[i], 20, 360 + i * 60, fnt, colour)
    return ent, btl_cmd
