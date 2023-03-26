import pygame
import random

BLACK = (0, 0, 0)
imgWall = pygame.image.load("image/wall.png")
imgWall2 = pygame.image.load("image/wall2.png")
imgDark = pygame.image.load("image/dark.png")
imgFloor = [
    pygame.image.load("image/base/floor.png"),
    pygame.image.load("image/tbox.png"),
    pygame.image.load("image/cocoon.png"),
    pygame.image.load("image/stairs.png")
]
imgShip = [
    pygame.image.load("image/character/ship0.png"),
    pygame.image.load("image/character/ship1.png"),
    pygame.image.load("image/character/ship2.png"),
    pygame.image.load("image/character/ship3.png"),
    pygame.image.load("image/character/ship4.png"),
    pygame.image.load("image/character/ship5.png"),
    pygame.image.load("image/character/ship6.png"),
    pygame.image.load("image/character/ship7.png"),
    pygame.image.load("image/character/ship8.png"),
]


# create dungeon method using maze
# return dungeon
def create_dungeon(
    maze_width: int,
    maze_height: int,
    dungeon_width: int,
    dungeon_height: int,
) -> list:
    # initiate maze
    maze = []
    for y in range(maze_height):
        maze.append([0] * maze_width)

    # list for creating wall
    x_list = [0, 1, 0, -1]
    y_list = [-1, 0, 1, 0]

    # rim wall = 1
    for x in range(maze_width):
        maze[0][x] = 1
        maze[maze_height - 1][x] = 1
    for y in range(1, maze_height - 1):
        maze[y][0] = 1
        maze[y][maze_width - 1] = 1

    # initiate inside room 0
    for y in range(1, maze_height - 1):
        for x in range(1, maze_width - 1):
            maze[y][x] = 0
    # pillar 1
    for y in range(2, maze_height - 2, 2):
        for x in range(2, maze_width - 2, 2):
            maze[y][x] = 1

    # create wall from pillar
    for y in range(2, maze_height - 2, 2):
        for x in range(2, maze_width - 2, 2):
            d = random.randint(0, 3)
            # Do not make a wall on the left from the second
            if x > 2:
                d = random.randint(0, 2)
            maze[y + y_list[d]][x + x_list[d]] = 1

    # initiate dungeon
    dungeon = []
    for y in range(dungeon_height):
        dungeon.append([0] * dungeon_width)

    # create dungeon from maze
    # all wall = 9
    for y in range(dungeon_height):
        for x in range(dungeon_width):
            dungeon[y][x] = 9

    # create room and aisle
    for y in range(1, maze_height - 1):
        for x in range(1, maze_width - 1):
            dx = x * 3 + 1
            dy = y * 3 + 1

            if maze[y][x] == 0:
                # create room at random
                if random.randint(0, 99) < 20:
                    # room 0, 3x3
                    for ry in range(-1, 2):
                        for rx in range(-1, 2):
                            dungeon[dy + ry][dx + rx] = 0
                # create aisle
                else:
                    dungeon[dy][dx] = 0
                    if maze[y - 1][x] == 0:
                        dungeon[dy - 1][dx] = 0
                    if maze[y + 1][x] == 0:
                        dungeon[dy + 1][dx] = 0
                    if maze[y][x - 1] == 0:
                        dungeon[dy][dx - 1] = 0
                    if maze[y][x + 1] == 0:
                        dungeon[dy][dx + 1] = 0
    return dungeon


# view dungeon
def view_dungeon(
    screen,
    ship_x: int,
    ship_y: int,
    dungeon: list,
    dungeon_width: int,
    dungeon_height: int,
    ship_animation: int,
):
    screen.fill(BLACK)
    # view from y -4 mass to y +5 mass
    # view from x -5 mass to y +5 mass
    for y in range(-4, 6):
        for x in range(-5, 6):
            X = (x + 5) * 80
            Y = (y + 4) * 80
            dx = ship_x + x
            dy = ship_y + y
            if 0 <= dx < dungeon_width and 0 <= dy < dungeon_height:
                # 0 floor, 1 box, 2 cocoon, 3 stars
                if dungeon[dy][dx] <= 3:
                    screen.blit(imgFloor[dungeon[dy][dx]], [X, Y])
                # 9 wall
                if dungeon[dy][dx] == 9:
                    screen.blit(imgWall, [X, Y - 40])
                    if dy >= 1 and dungeon[dy - 1][dx] == 9:
                        screen.blit(imgWall2, [X, Y - 80])
            # view ship in the center
            if x == 0 and y == 0:
                screen.blit(imgShip[ship_animation], [X, Y - 40])
    # view dark
    screen.blit(imgDark, [0, 0])
