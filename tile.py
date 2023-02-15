import pygame
from utils import *


class Tile:
    def __init__(self, x: int, y: int, bomb: bool):
        self.x, self.y, self.bomb = x, y, bomb
        self.clicked = False

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, 16, 16)

    def draw(self, screen: pygame.Surface):
        draw_frame(screen, self.rect, frame_width=1)
