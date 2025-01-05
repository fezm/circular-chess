from constants import *


class Move():
    # Represents a chess move
    ann_to_rank = {0: '1', 1: '2', 2: '3', 3: '4'}
    rank_to_ann = {v: k for k, v in ann_to_rank.items()}

    sect_to_file = {0: 'l', 1: 'k', 2: 'j', 3: 'i', 4: 'h', 5: 'g', 6: 'f', 7: 'e',
                    8: 'd', 9: 'c', 10: 'b', 11: 'a', 12: 'p', 13: 'o', 14: 'n', 15: 'm'}
    file_to_sect = {v: k for k, v in sect_to_file.items()}

    def __init__(self, start_space, end_space, board):
        # Initializes a move
        self.start_ann = start_space[0]
        self.start_sect = start_space[1]

        self.end_ann = end_space[0]
        self.end_sect = end_space[1]

        self.piece_moved = board[self.start_ann][self.start_sect]
        self.piece_captured = board[self.end_ann][self.end_sect]

        self.move_id = self.start_ann * 1000 + self.start_sect * 100 + \
            self.end_ann * 10 + self.end_sect

    def __eq__(self, other):
        # Overrides the equals method
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        # Gets the chess notation for the move
        piece_char = ''
        if self.piece_moved[1] != 'p':
            piece_char = self.piece_moved[1]

        if self.piece_captured == "--":
            return piece_char + self.get_file_rank(self.end_ann, self.end_sect)
        else:
            piece2_char = ''
            if self.piece_captured[1] != 'p':
                piece2_char = self.piece_captured[1]
            return piece_char + self.get_file_rank(self.start_ann, self.start_sect) + 'x' + piece2_char + self.get_file_rank(self.end_ann, self.end_sect)

    def get_file_rank(self, a, sect):
        # Gets the file and rank for a given position
        return self.sect_to_file[sect] + self.ann_to_rank[a]
