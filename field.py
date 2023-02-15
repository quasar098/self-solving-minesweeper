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
                column.append(Tile(x*16+15, y*16+11, False))
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

    def draw(self, screen: pygame.Surface):
        for column in self.tiles:
            for tile in column:
                tile.draw(screen)
