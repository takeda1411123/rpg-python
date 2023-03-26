

BLACK = (0, 0, 0)


# view text with shadow
def view_text(screen, text, x, y, fnt, col):
    # shadow
    sur = fnt.render(text, True, BLACK)
    screen.blit(sur, [x + 1, y + 2])
    # text
    sur = fnt.render(text, True, col)
    screen.blit(sur, [x, y])
