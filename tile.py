import pygame
from utils import *


class Tile:
    def __init__(self, x: int, y: int, bomb: bool, real_pos: tuple[int, int], field=None):
        self.x, self.y, self.bomb = x, y, bomb
        self.real = real_pos
        self.clicked = False
        self.flagged = False
        self.field = field
        self.override = None

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, 16, 16)

    @property
    def pos(self):
        return self.x, self.y

    def override_num(self, num: int):
        self.override = num

    def draw(self, screen: pygame.Surface):
        # draw indent if not clicked
        if not self.clicked:
            draw_frame(screen, self.rect, frame_width=2)
            if self.flagged:
                draw_flag(screen, self.pos)
            return
        pygame.draw.rect(screen, FRAME_DARK, self.rect)
        pygame.draw.rect(screen, BG_COLOR, self.rect.move(1, 1).inflate(-1, -1))
        draw_num(screen, self.pos, self.field.get_number(*self.real))

    def click(self, screen: pygame.Surface):
        assert not self.flagged, "dont click flagged tile"
        if not self.clicked:
            self.clicked = True
            self.draw(screen)
            dirty_rects.append(self.rect)

    def flag(self, screen: pygame.Surface):
        assert not self.clicked, "dont click flagged tile"
        if not self.flagged:
            self.flagged = True
            self.draw(screen)
            dirty_rects.append(self.rect)
