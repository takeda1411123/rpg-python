import random


# set event
def set_event(
    dungeon_width: int,
    dungeon_height: int,
    dungeon: list,
):
    # stair
    while True:
        x = random.randint(3, dungeon_width - 4)
        y = random.randint(3, dungeon_height - 4)
        # if mass is floor, create stair
        if dungeon[y][x] == 0:
            # change from wall to floor around stair
            for ry in range(-1, 2):
                for rx in range(-1, 2):
                    dungeon[y + ry][x + rx] = 0
            dungeon[y][x] = 3
            break
    # box and cocoon
    # 1 is box, 2 is cocoon
    for i in range(60):
        x = random.randint(3, dungeon_width - 4)
        y = random.randint(3, dungeon_height - 4)
        # if mass is floor, create cocoon or box
        if dungeon[y][x] == 0:
            dungeon[y][x] = random.choice([1, 2, 2, 2, 2])
    # ship position
    while True:
        ship_xposition = random.randint(3, dungeon_width - 4)
        ship_yposition = random.randint(3, dungeon_height - 4)
        if dungeon[ship_yposition][ship_xposition] == 0:
            break

    # ship facade
    ship_direction = 1
    ship_animation = 2
    return dungeon, ship_xposition, ship_yposition, ship_direction, ship_animation
