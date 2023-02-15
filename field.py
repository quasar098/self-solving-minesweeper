import pygame
from utils import *
from tile import Tile
from random import randint as rand


class Field:
    def __init__(self, rect: pygame.Rect):
        self.rect = rect
        if self.rect.width % 16 or self.rect.height % 16:
            # each minesweeper tile is 16 by 16, so having extra space is bad
            print("Your monitor is non-standard! This may cause some graphical glitches")
        self.width = self.rect.width//16
        self.height = self.rect.height//16
        self.tiles = []
        for x in range(self.width):
            column = []
            for y in range(self.height):
                column.append(Tile(x*16+15, y*16+11, False, (x, y), self))
            self.tiles.append(column)
        self.randomize_bombs()

    @property
    def tile_count(self):
        return self.width*self.height

    def randomize_bombs(self):
        bomb_num = int(self.tile_count*BOMB_PERCENT/100)
        while bomb_num != 0:
            posx, posy = rand(0, self.width-1), rand(0, self.height-1)
            if self.tiles[posx][posy].bomb:
                continue
            self.tiles[posx][posy].bomb = True
            bomb_num -= 1

    def get_number(self, x: int, y: int):
        total = 0
        if self.tiles[x][y].override:
            return self.tiles[x][y].override

        for xo in range(-1, 2):
            for yo in range(-1, 2):
                if not xo and not yo:
                    continue
                try:
                    real = self.tiles[xo+x][yo+y]
                except IndexError:
                    continue
                if real.bomb:
                    total += 1
        return total

    def draw(self, screen: pygame.Surface):
        for column in self.tiles:
            for tile in column:
                tile.draw(screen)

    def do(self, screen: pygame.Surface):
        for _ in range(1, 9):
            self.tiles[_][1].override_num(_)
            self.tiles[_][1].click(screen)
