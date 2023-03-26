import pygame

from text import view_text

WHITE = (255, 255, 255)
RED = (255, 0, 0)

# character image
imgLuffy = pygame.image.load("image/character/luffy.png")
imgGaze = pygame.image.load("image/gaze.png")
imgGazeChopper = pygame.image.load("image/character/chopperS.png")
imgGazeFlag = pygame.image.load("image/character/flagS.png")


# view user score
def view_ship_score(
    screen, fnt,
    ship_life, ship_life_max, ship_str, food,
    chopper_cure, zoro,
    tmr
):
    # add luffy
    screen.blit(imgLuffy, [30, 600])

    # base position
    x = 120
    y = 600
    screen.blit(imgGaze, [x, y])
    screen.blit(imgGazeChopper, [271, y])
    screen.blit(imgGazeFlag, [269, y+29])

    # basic white
    col = WHITE
    # when barely dead, colour red
    if ship_life < 10 and tmr % 2 == 0:
        col = RED
    view_text(screen, "{}/{}".format(ship_life, ship_life_max), x + 60, y + 3, fnt, col)
    view_text(screen, str(ship_str), x + 60, y + 30, fnt, WHITE)
    col = WHITE
    if food == 0 and tmr % 2 == 0:
        col = RED
    view_text(screen, str(food), x + 60, y + 57, fnt, col)
    view_text(screen, str(chopper_cure), x + 190, y + 3, fnt, WHITE)
    view_text(screen, str(zoro), x + 190, y + 30, fnt, WHITE)

    return