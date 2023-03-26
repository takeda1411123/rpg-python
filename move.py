import pygame
import random
from pygame.locals import *


# move ship
def move_ship(
    key,
    dungeon: list,
    ship_xposition: int, ship_ypostition: int, ship_direction: int, ship_animation: int,
    ship_life: int, ship_life_max: int, chopper_cure: int, zoro: int, food: int,
    idx: int, tmr: int,
    treasure: int,
):
    # 1 is box
    if dungeon[ship_ypostition][ship_xposition] == 1:
        (
            dungeon,
            chopper_cure, zoro, food, idx, tmr,
            treasure
        ) = get_box(
            dungeon,
            ship_xposition, ship_ypostition,
            chopper_cure, zoro, food
        )
        return (
            dungeon,
            ship_xposition, ship_ypostition, ship_direction, ship_animation,
            ship_life, ship_life_max, chopper_cure, zoro, food,
            idx, tmr,  # 3 get item
            treasure
        )

    # 2 is cocoon
    if dungeon[ship_ypostition][ship_xposition] == 2:
        (
            dungeon,
            food,
            idx, tmr,
            treasure,
        ) = get_cocoon(
            dungeon,
            ship_xposition, ship_ypostition,
            food,
            treasure,
        )
        return (
            dungeon,
            ship_xposition, ship_ypostition, ship_direction, ship_animation,
            ship_life, ship_life_max, chopper_cure, zoro, food,
            idx, tmr,  # 3 get item or 10 battle start
            treasure
        )
    # 3 is stair
    if dungeon[ship_ypostition][ship_xposition] == 3:
        return (
            dungeon,
            ship_xposition, ship_ypostition, ship_direction, ship_animation,
            ship_life, ship_life_max, chopper_cure, zoro, food,
            2, 0,  # next floor
            treasure
        )

    # step ship
    # decrease food or ship life
    (
        dungeon,
        ship_xposition, ship_ypostition, ship_direction, ship_animation,
        food, ship_life,
        idx, tmr,
    ) = step_ship(
        key, dungeon,
        ship_xposition, ship_ypostition, ship_direction,
        food, ship_life, ship_life_max,
        idx, tmr
    )
    return (
        dungeon,
        ship_xposition, ship_ypostition, ship_direction, ship_animation,
        ship_life, ship_life_max, chopper_cure, zoro, food,
        idx, tmr,
        treasure
    )


# event box
def get_box(
    dungeon: list,
    ship_xposition: int,
    ship_ypostition: int,
    chopper_cure: int,
    zoro: int,
    food: int,
):
    # banish box
    dungeon[ship_ypostition][ship_xposition] = 0
    treasure = random.choice([0, 0, 0, 1, 1, 1, 1, 1, 1, 2])
    # chopper_cure
    if treasure == 0:
        chopper_cure = chopper_cure + 1
    # zoro
    if treasure == 1:
        zoro = zoro + 1
    # food
    if treasure == 2:
        food = int(food / 2)
    # view getting item
    idx = 3
    tmr = 0

    return (
        dungeon,
        chopper_cure, zoro, food,
        idx, tmr,
        treasure
    )


# event cocoon
def get_cocoon(
    dungeon: list,
    ship_xposition: int,
    ship_ypostition: int,
    food: int,
    treasure: int,
):
    # banish box
    dungeon[ship_ypostition][ship_xposition] = 0
    # random food or enemy
    r = random.randint(0, 99)
    if r < 40:
        # get food
        treasure = random.choice([3, 3, 3, 4])
        if treasure == 3:
            food = food + 20
        if treasure == 4:
            food = food + 100
        # view getting item
        idx = 3
        tmr = 0
    else:
        # battle start
        idx = 10
        tmr = 0

    return (
        dungeon,
        food,
        idx, tmr,
        treasure
    )


# step ship
def step_ship(
    key,
    dungeon: list,
    ship_xposition: int,
    ship_ypostition: int,
    ship_direction: int,
    food: int,
    ship_life: int,
    ship_life_max: int,
    idx: int,
    tmr: int,
):
    # ↑↓→← step
    x = ship_xposition
    y = ship_ypostition
    # ↑
    if key[K_UP] == 1:
        # back
        ship_direction = 0
        # dungeon 9 is a wall
        if dungeon[ship_ypostition - 1][ship_xposition] != 9:
            ship_ypostition = ship_ypostition - 1
    #  ↓
    if key[K_DOWN] == 1:
        # facade
        ship_direction = 1
        if dungeon[ship_ypostition + 1][ship_xposition] != 9:
            ship_ypostition = ship_ypostition + 1
    #  ←
    if key[K_LEFT] == 1:
        # left
        ship_direction = 2
        if dungeon[ship_ypostition][ship_xposition - 1] != 9:
            ship_xposition = ship_xposition - 1
    #  →
    if key[K_RIGHT] == 1:
        # right
        ship_direction = 3
        if dungeon[ship_ypostition][ship_xposition + 1] != 9:
            ship_xposition = ship_xposition + 1

    # change image according direction
    ship_animation = ship_direction * 2
    # if ship move, 移動したら食料の量と体力を計算
    if ship_xposition != x or ship_ypostition != y:
        ship_animation = ship_animation + tmr % 2  # 移動したら足踏みのアニメーション
        # first decrease food, second decrease ship life
        if food > 0:
            food = food - 1
            if ship_life < ship_life_max:
                ship_life = ship_life + 1
        else:
            ship_life = ship_life - 5
            if ship_life <= 0:
                ship_life = 0
                pygame.mixer.music.stop()
                # game over
                idx = 9
                tmr = 0

    return (
        dungeon,
        ship_xposition, ship_ypostition, ship_direction, ship_animation,
        food, ship_life,
        idx, tmr,
    )
