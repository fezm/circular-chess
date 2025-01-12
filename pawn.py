from constants import *

LEFT_WHITE = 0
RIGHT_WHITE = 1
LEFT_BLACK = 2
RIGHT_BLACK = 3

PAWN_WHITE = 'w'
PAWN_BLACK = 'b'

start_sectors = {LEFT_WHITE: 13, RIGHT_WHITE: 10,
                 LEFT_BLACK: 2, RIGHT_BLACK: 5}
end_sectors = {LEFT_WHITE: 3, RIGHT_WHITE: 4, LEFT_BLACK: 12, RIGHT_BLACK: 11}


class Pawn:
    def __init__(self, sector, color):
        # Initializes a pawn
        self.color = color
        self.sector = sector
        self.on_left_half = self._is_on_left_half()
        self.dir = self._get_pawn_dir()
        self.start_sector = self._get_start_sector()
        self.end_sector = self._get_end_sector()

    def _is_on_left_half(self):
        """Determine if the pawn is on the left half of the board."""
        return self.sector <= 3 or self.sector >= 12

    def _get_pawn_dir(self):
        """Determine the movement direction of the pawn."""
        direction = 1 if self.color == PAWN_WHITE else -1
        return direction if self.on_left_half else -direction

    def _get_key(self):
        """Determine the key for start and end sector lookups."""
        if self.color == PAWN_WHITE:
            return LEFT_WHITE if self.on_left_half else RIGHT_WHITE
        else:
            return LEFT_BLACK if self.on_left_half else RIGHT_BLACK

    def _get_start_sector(self):
        """Get the starting sector for this pawn."""
        return start_sectors[self._get_key()]

    def _get_end_sector(self):
        """Get the ending sector for this pawn."""
        return end_sectors[self._get_key()]

    def update_sector(self, new_sector):
        """Update the pawn's current sector and movement status."""
        self.sector = new_sector
        self.has_moved = self._has_moved_fun()
        return
