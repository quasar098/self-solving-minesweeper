import pygame
from utils import *
from field import Field

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.NOFRAME)

five_inside_rect = screen.get_rect().inflate(-26, -18)

field = Field(five_inside_rect.inflate(-6, -6))

running = True
while running:
    screen.fill(BG_COLOR)
    for event in pygame.event.get():
        # this is a screensaver, so any input just stops the screensaver (that's the point)

        # todo: uncomment below
        # if event.type == pygame.KEYDOWN:
        #     running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # do not cancel screensaver on mouse scroll because sometimes i randomly scroll the mouse for fun
            if event.button in (4, 5):
                continue
            running = False

    # draw frames like windows xp minesweeper
    draw_frame(screen, screen.get_rect())
    draw_inverse_frame(screen, five_inside_rect)
    field.draw(screen)

    pygame.display.flip()
    clock.tick(FRAMERATE)
pygame.quit()
