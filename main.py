from win32api import GetSystemMetrics
import pygame
from utils import *

pygame.init()

WIDTH, HEIGHT = [GetSystemMetrics(screen_size) for screen_size in range(2)]
FRAMERATE = 75

clock = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.NOFRAME)

five_inside_rect = screen.get_rect().inflate(-26, -26)

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

    pygame.display.flip()
    clock.tick(FRAMERATE)
pygame.quit()
