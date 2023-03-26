import pygame
import sys

WHITE = (255, 255, 255)

# define back
imgBack = None
imgEnemy = None

enemy_number = 0
back_number = 0
enemy_x = 0
enemy_y = 0


# initiate
def init():
    global imgBack, imgEnemy, enemy_number, back_number, enemy_x, enemy_y
    enemy_number = enemy_number + 1
    back_number = back_number + 1
    if enemy_number == 5:
        enemy_number = 1
    if back_number == 4:
        back_number = 1
    # load image
    imgBack = pygame.image.load("image/back"+str(back_number)+".jpeg")
    imgEnemy = pygame.image.load("image/enemy"+str(enemy_number)+".png")

    # define image position
    enemy_x = 440-imgEnemy.get_width()/2
    enemy_y = 450-imgEnemy.get_height()


def draw_battle(screen, fnt):
    screen.blit(imgBack, [0, 0])
    screen.blit(imgEnemy, [enemy_x, enemy_y])
    sur = fnt.render("image/enemy"+str(enemy_number)+".png", True, WHITE)
    screen.blit(sur, [300, 450])


def main():
    pygame.init()
    pygame.display.set_caption("battle start")
    screen = pygame.display.set_mode((880, 600))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)

    init()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    init()

        draw_battle(screen, font)
        pygame.display.update()
        clock.tick(5)


if __name__ == '__main__':
    main()