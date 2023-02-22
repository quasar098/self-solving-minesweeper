import functools
from os.path import join
from random import randint as rand, choice

from tile import Tile
from utils import *


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = perf_counter()
        value = func(*args, **kwargs)
        toc = perf_counter()
        elapsed_time = toc - tic
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")
        return value
    return wrapper_timer


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

    @property
    def tile_count(self):
        return self.width * self.height

    def randomize_bombs(self):
        for column in self.tiles:
            for tile in column:
                tile.bomb = False
                tile.clicked = False
                tile.flagged = False
                tile.satisfied = False
                tile.draw(pygame.display.get_surface())
        bomb_num = int(self.tile_count * BOMB_PERCENT / 100)
        while bomb_num != 0:
            posx, posy = rand(0, self.width - 1), rand(0, self.height - 1)
            if self.tiles[posx][posy].bomb:
                continue
            self.tiles[posx][posy].bomb = True
            bomb_num -= 1

        if not PLAYABLE:
            middle = (self.width//2, self.height//2)
            if self.get_number(*middle):
                self.randomize_bombs()

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
                if not (0 <= xo + x < self.width):
                    continue
                if not (0 <= yo + y < self.height):
                    continue
                if real.bomb:
                    total += 1
        return total

    def get_neighbor_tiles(self, x: int, y: int, tl: list[list[Tile]] = None):
        if tl is None:
            tl = self.tiles
        if tl[x][y].override:
            return tl[x][y].override

        total = []
        for xo in range(-1, 2):
            for yo in range(-1, 2):
                if not xo and not yo:
                    continue

                if not (0 <= xo + x < self.width):
                    continue
                if not (0 <= yo + y < self.height):
                    continue

                try:
                    real = tl[xo + x][yo + y]
                except IndexError:
                    continue

                total.append(real)
        return total

    def draw(self, screen: pygame.Surface):
        for column in self.tiles:
            for tile in column:
                tile.draw(screen)

    def cascade(self, pos: tuple[int, int]):
        # first tile cannot be mine
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
            if tile.click(pygame.display.get_surface()):
                return True

            if rand(1, 10) == 4:
                self.handle_all()

            pygame.time.wait(ANIM_SPEED)
            update_screen()
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

    def register(self, event: pygame.event.Event):
        mp = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for column in self.tiles:
                    for tile in column:
                        if tile.rect.collidepoint(mp):
                            if self.cascade(tile.real):
                                self.randomize_bombs()
                                pygame.display.flip()
                            return True
            if event.button == 3:
                for column in self.tiles:
                    for tile in column:
                        if tile.rect.collidepoint(mp):
                            tile.flag_toggle(pygame.display.get_surface())
                            return True

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         self.do(pygame.display.get_surface())

        if self.complete:
            Field.show_win_anim()
            self.randomize_bombs()
            self.draw(pygame.display.get_surface())
            pygame.display.flip()

        return False
    
    @property
    def complete(self):
        all_mystery = [tile for column in self.tiles for tile in column if not tile.clicked and not tile.flagged]
        return len(all_mystery) == 0

    @property
    def mine_counts(self):
        total = []
        for column in self.tiles:
            row = []
            for tile in column:
                row.append(self.get_number(*tile.real))
            total.append(row)
        return total

    @staticmethod
    def show_win_anim():
        win_picture = pygame.image.load(join("assets", "win.png"))
        pygame.display.get_surface().blit(
            win_picture,
            win_picture.get_rect(center=pygame.display.get_surface().get_rect().center)
        )
        pygame.display.flip()
        pygame.time.wait(1000)

    def handle_all(self):
        for event in pygame.event.get():

            # this is a screensaver, so any input just stops the screensaver (that's the point)
            if not PLAYABLE:
                if event.type == pygame.KEYDOWN:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button in (1, 2, 3):
                    pygame.quit()
                    quit()

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()

                self.register(event)

    def do(self, screen: pygame.Surface):

        hash_before = hash(str(self.tiles))

        mine_counts_cache = self.mine_counts

        # flag stuff
        for x, column in sorted(enumerate(self.tiles), key=lambda _: rand(1, 100)):
            for y, tile in enumerate(column):

                if not tile.clicked:
                    continue

                if tile.satisfied:
                    continue

                num_surrounding = mine_counts_cache[x][y]
                unclicked = [mine for mine in self.get_neighbor_tiles(x, y)
                             if not mine.clicked]
                if num_surrounding == len(unclicked):
                    changed = False
                    for neighbor in unclicked:
                        before = neighbor.flagged
                        neighbor.flag(screen)
                        if not before and neighbor.flagged:
                            changed = True
                    tile.satisfied = True

                    if changed:
                        pygame.time.wait(ANIM_SPEED * 4)
                        update_screen()

                self.handle_all()

        self.handle_all()

        mine_counts_cache = self.mine_counts
        for x, column in sorted(enumerate(self.tiles), key=lambda _: rand(1, 4)):
            for y, tile in sorted(enumerate(column), key=lambda _: rand(1, 4)):

                if not tile.clicked:
                    continue

                flagged_neighbors = [mine for mine in self.get_neighbor_tiles(x, y)
                                     if (not mine.clicked) and mine.flagged]
                unclicked_neighbors = [mine for mine in self.get_neighbor_tiles(x, y)
                                       if not mine.clicked]
                if mine_counts_cache[x][y] == len(flagged_neighbors):
                    for neighbor in unclicked_neighbors:
                        if neighbor not in flagged_neighbors:
                            self.cascade(neighbor.real)
                self.handle_all()

        hash_after = hash(str(self.tiles))

        if self.complete:
            Field.show_win_anim()
            self.randomize_bombs()
            self.draw(screen)
            pygame.display.flip()
            return

        if hash_before == hash_after:
            all_mystery = [tile for column in self.tiles for tile in column if not tile.clicked and not tile.flagged]
            override_pos = None
            if len(all_mystery) == self.width*self.height:
                override_pos = (self.width//2, self.height//2)
            else:
                if RNG_CARRY:
                    all_mystery = [allm for allm in all_mystery if not allm.bomb]

            assert len(all_mystery), "this should not happen"

            done_it = False
            while not done_it:
                if override_pos is None:
                    tile = choice(all_mystery)
                else:
                    tile = self.tiles[override_pos[0]][override_pos[1]]
                if not tile.clicked and not tile.flagged:
                    if tile.click(screen):
                        self.randomize_bombs()
                        self.draw(screen)
                        pygame.display.flip()
                    done_it = True
