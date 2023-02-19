import pygame
from utils import *
from field import Field


def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.NOFRAME)

    five_inside_rect = screen.get_rect().inflate(-26, -18)

    field = Field(five_inside_rect.inflate(-6, -6))

    screen.fill(BG_COLOR)
    draw_frame(screen, screen.get_rect())
    draw_inverse_frame(screen, five_inside_rect)
    field.draw(screen)
    pygame.display.flip()

    while True:
        field.handle_all()
        if not PLAYABLE:
            field.do(screen)

        update_screen()
        clock.tick(FRAMERATE)


if __name__ == '__main__':
    main()
