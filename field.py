import pygame
from utils import *
from tile import Tile
from random import randint as rand


class Field:
    def __init__(self, rect: pygame.Rect):
        self.rect = rect
        self.first_cascade_done = False
        if self.rect.width % 16 or self.rect.height % 16:
            # each minesweeper tile is 16 by 16, so having extra space is bad
            print("Your monitor is non-standard! This may cause some graphical glitches")
        self.width = self.rect.width // 16
        self.height = self.rect.height // 16
        self.tiles = []
        for x in range(self.width):
            column = []
            for y in range(self.height):
                column.append(Tile(x * 16 + 15, y * 16 + 11, False, (x, y), self))
            self.tiles.append(column)
        self.randomize_bombs()
        self.cascade((30, 30))  # todo remove this

    @property
    def tile_count(self):
        return self.width * self.height

    def randomize_bombs(self):
        for column in self.tiles:
            for tile in column:
                tile.bomb = False
        bomb_num = int(self.tile_count * BOMB_PERCENT / 100)
        while bomb_num != 0:
            posx, posy = rand(0, self.width - 1), rand(0, self.height - 1)
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
                    real = self.tiles[xo + x][yo + y]
                except IndexError:
                    continue
                if real.bomb:
                    total += 1
        return total

    def draw(self, screen: pygame.Surface):
        for column in self.tiles:
            for tile in column:
                tile.draw(screen)

    def cascade(self, pos: tuple[int, int]):
        if not self.first_cascade_done:
            while self.get_number(*pos):
                self.randomize_bombs()
            self.first_cascade_done = True
        queue = [pos]
        seen = []
        while len(queue):
            tx, ty = queue[0]
            queue.pop(0)
            if (tx, ty) in seen:
                continue
            tile = self.tiles[tx][ty]
            tile.click(pygame.display.get_surface())
            if self.get_number(tx, ty) == 0:
                neighbors = self.get_neighbor_positions((tx, ty))
                for neighbor in neighbors:
                    queue.append(neighbor)
            seen.append((tx, ty))

    def get_neighbor_positions(self, pos: tuple[int, int]):
        return [_ for _ in
                [move_pos(pos, (ox, oy)) for ox in range(-1, 2) for oy in range(-1, 2) if ox != 0 or oy != 0]
                if 0 <= _[0] < self.width and 0 <= _[1] < self.height
                ]

    def do(self, screen: pygame.Surface):
        pass
