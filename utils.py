import pygame
import pygame.gfxdraw


# colors
BG_COLOR = pygame.Color(192, 192, 192)
FRAME_DARK = pygame.Color(135, 136, 143)
FRAME_LIGHT = pygame.Color(255, 255, 255)


def move_pos(base: tuple[int, int], moved: tuple[int, int]):
    return base[0] + moved[0], base[1] + moved[1]


def draw_frame(screen: pygame.Surface, rect: pygame.Rect, frame_width=3):
    # draws a minesweeper style frame around a specified rectangle
    pygame.draw.line(
        screen, FRAME_DARK,
        move_pos(rect.bottomleft, (3 - frame_width, 1 - frame_width)),
        move_pos(rect.bottomright, (1 - frame_width, 1 - frame_width)),
        width=3
    )
    pygame.draw.line(
        screen, FRAME_DARK,
        move_pos(rect.topright, (1 - frame_width, 3 - frame_width)),
        move_pos(rect.bottomright, (1 - frame_width, 1 - frame_width)),
        width=frame_width
    )
    pygame.draw.line(
        screen, FRAME_LIGHT,
        move_pos(rect.topleft, (1, 1)),
        move_pos(rect.bottomleft, (1, -1)),
        width=frame_width
    )
    pygame.draw.line(
        screen, FRAME_LIGHT,
        move_pos(rect.topleft, (1, 1)),
        move_pos(rect.topright, (-1, 1)),
        width=frame_width
    )
    for frame_smooth in range(frame_width):
        for frame_replace in range(1, frame_smooth+1):
            pygame.gfxdraw.pixel(screen, rect.left + frame_smooth,
                                 rect.bottom - 1 - frame_smooth + frame_replace, FRAME_DARK)
        pygame.gfxdraw.pixel(screen, rect.left + frame_smooth, rect.bottom - 1 - frame_smooth, BG_COLOR)

    for frame_smooth in range(frame_width):
        for frame_replace in range(1, frame_smooth+1):
            pygame.gfxdraw.pixel(screen, rect.right + frame_smooth - frame_width,
                                 rect.top - 1 - frame_smooth + frame_replace + frame_width, FRAME_DARK)
        pygame.gfxdraw.pixel(screen, rect.right + frame_smooth - frame_width,
                             rect.top - 1 - frame_smooth + frame_width, BG_COLOR)

    pygame.gfxdraw.pixel(screen, rect.left, rect.top, FRAME_LIGHT)
    pygame.gfxdraw.pixel(screen, rect.right-1, rect.bottom-1, FRAME_DARK)


def draw_inverse_frame(screen: pygame.Surface, rect: pygame.Rect, frame_width=3):
    # very bad solution to this but whatever
    global FRAME_DARK, FRAME_LIGHT
    old_light, old_dark = FRAME_LIGHT, FRAME_DARK
    FRAME_DARK, FRAME_LIGHT = FRAME_LIGHT, FRAME_DARK
    draw_frame(screen, rect, frame_width)
    FRAME_DARK, FRAME_LIGHT = old_dark, old_light
