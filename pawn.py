from constants import *

LEFT_WHITE = 0
RIGHT_WHITE = 1
LEFT_BLACK = 2
RIGHT_BLACK = 3

PAWN_WHITE = 'w'
PAWN_BLACK = 'b'


end_sectors = {LEFT_WHITE: 3, RIGHT_WHITE: 4, LEFT_BLACK: 12, RIGHT_BLACK: 11}


class Pawn:
    def __init__(self, sector, color):
        # Initializes a pawn
        self.color = color
        self.sector = sector
        self.on_left_half = self.on_left_half_fun()
        self.dir = self.get_pawn_dir()
        self.end_sector = self.get_end_sector()
        self.has_moved = self.has_moved_fun()

    def on_left_half_fun(self):
        return self.sector <= 3 or self.sector >= 12

    def get_pawn_dir(self):
        direction = 1 if self.color == PAWN_WHITE else -1
        return direction if self.on_left_half else -direction

    def get_end_sector(self):
        key = LEFT_WHITE if self.color == PAWN_WHITE and self.on_left_half else \
            RIGHT_WHITE if self.color == PAWN_WHITE else \
            LEFT_BLACK if self.on_left_half else \
            RIGHT_BLACK
        return end_sectors[key]

    def has_moved_fun(self):
        # TODO
        return

    def update_sector(self, new_sector):
        self.sector = new_sector
        self.has_moved = self.has_moved_fun()
        return