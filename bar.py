import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# view enemy score
def view_enemy_score(bg, x, y, w, h, val, max):
    pygame.draw.rect(bg, WHITE, [x - 2, y - 2, w + 4, h + 4])
    pygame.draw.rect(bg, BLACK, [x, y, w, h])
    if val > 0:
        pygame.draw.rect(bg, (0, 128, 255), [x, y, w * val / max, h])