import numpy as np
import pygame as pg
import pygame.gfxdraw
from constants import *


class Board:
    def __init__(self):
        # board is a 4x16 2d list, each entry has 2 characters
        # first character represents color: 'b' or 'w'
        # second character represents type of piece: 'K', 'Q', 'R', 'B', 'N', 'p'
        # "--" represents an empty square
        self.board = [
            ["--", "--", "bp", "bQ", "bK", "bp", "--", "--",
             "--", "--", "wp", "wK", "wQ", "wp", "--", "--"],
            ["--", "--", "bp", "bB", "bB", "bp", "--", "--",
             "--", "--", "wp", "wB", "wB", "wp", "--", "--"],
            ["--", "--", "bp", "bN", "bN", "bp", "--", "--",
             "--", "--", "wp", "wN", "wN", "wp", "--", "--"],
            ["--", "--", "bp", "bR", "bR", "bp", "--", "--",
             "--", "--", "wp", "wR", "wR", "wp", "--", "--"]
        ]

        self.white_to_move = True

        self.move_log = []

    def fill_arc(self, window, center, radius, theta0, theta1, color, ndiv=150):
        x0, y0 = center

        dtheta = (theta1 - theta0) / ndiv
        angles = [theta0 + i*dtheta for i in range(ndiv + 1)]

        points = [(x0, y0)] + [(x0 + radius * np.cos(theta), y0 -
                                radius * np.sin(theta)) for theta in angles]

        pygame.gfxdraw.filled_polygon(window, points, color)

    def draw_board(self, window):

        # window.fill(GRAY)
        # self.fill_arc(window, CENTER, WIDTH//2, 0, pi, RED)
        # self.fill_arc(window, CENTER, WIDTH//2, pi, 2*pi, BLUE)

        for ring in range(ANNULI):
            radius = WIDTH//2 - ring*SPACING
            for sector in range(SECTORS):
                color = DARK if ((sector+ring) % 2) else LIGHT

                self.fill_arc(window, CENTER, radius, sector *
                              SLICE, (sector+1)*SLICE, color)

        pg.draw.circle(window, GRAY, CENTER, MIDDLE_RADIUS)
        # pg.draw.circle(window, RED, CENTER, cc_rad + spacing)

    def draw_pieces(self, window, images):
        x0, y0 = CENTER
        theta0 = SLICE / 2
        r0 = MIDDLE_RADIUS
        for a in range(ANNULI):
            r = r0 + (SPACING * a)
            r *= SCALING
            for sect in range(SECTORS):
                piece = self.board[a][sect]
                if piece != "--":

                    theta = theta0 + (SLICE * sect)

                    if sect >= 0 and sect < 4:
                        # top left
                        x = x0 + ((r * np.cos(pi - theta))) - (PIECE_SIZE/2)
                        y = y0 - ((r * np.sin(pi - theta))) - (PIECE_SIZE/2)
                    elif sect >= 4 and sect < 8:
                        # top right
                        x = x0 - (r * np.cos(theta)) - (PIECE_SIZE/2)
                        y = y0 - (r * np.sin(theta)) - (PIECE_SIZE/2)
                    elif sect >= 8 and sect < 12:
                        # bottom right
                        x = x0 + (r * np.cos(pi - theta)) - (PIECE_SIZE/2)
                        y = y0 - (r * np.sin(pi - theta)) - (PIECE_SIZE/2)
                    elif sect >= 12 and sect < 16:
                        # bottom left
                        x = x0 + (r * np.cos(pi - theta)) - (PIECE_SIZE/2)
                        y = y0 - (r * np.sin(pi - theta)) - (PIECE_SIZE/2)

                    window.blit(images[piece], pg.Rect(
                        x, y, PIECE_SIZE, PIECE_SIZE))

    def draw(self, window, images):
        self.draw_board(window)
        self.draw_pieces(window, images)

    def make_move(self, move):
        self.board[move.start_ann][move.start_sect] = "--"
        self.board[move.end_ann][move.end_sect] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_ann][move.start_sect] = move.piece_moved
            self.board[move.end_ann][move.end_sect] = move.piece_captured
            self.white_to_move = not self.white_to_move

    def get_valid_moves(self):
        return self.get_all_moves()

    def get_all_moves(self):
        moves = []
        for a in range(ANNULI):
            for sect in range(SECTORS):
                turn = self.board[a][sect][0]
                if (turn == 'w' and self.white_to_move) or \
                        (turn == 'b' and not self.white_to_move):
                    piece = self.board[a][sect][1]
                    if piece == 'p':
                        self.get_pawn_moves(a, sect, moves)
                    elif piece == 'R':
                        self.get_rook_moves(a, sect, moves)
        return moves

    def get_pawn_moves(self, a, sect, moves):
        on_right_half = sect > 4 and sect < 11
        on_left_half_W = (sect > 12 and sect < 15) or (sect >= 0 and sect < 3)
        on_left_half_B = (sect > 12 and sect <= 15) or (sect > 0 and sect < 3)

        if self.white_to_move:
            # one-square pawn move
            if on_right_half:
                if self.board[a][sect - 1] == "--":
                    moves.append(Move((a, sect), (a, sect - 1), self.board))
                    # two-square pawn move
                    if sect == 10 and self.board[a][sect - 2] == "--":
                        moves.append(
                            Move((a, sect), (a, sect - 2), self.board))
            elif on_left_half_W:
                if self.board[a][sect + 1] == "--":
                    moves.append(Move((a, sect), (a, sect + 1), self.board))
                    # two square pawn move
                    if sect == 13 and self.board[a][sect + 2] == "--":
                        moves.append(
                            Move((a, sect), (a, sect + 2), self.board))
            elif sect == 15 and self.board[a][0] == "--":
                moves.append(Move((a, sect), (a, 0), self.board))

            # captures
            if a - 1 >= 0:
                if on_right_half:
                    if self.board[a - 1][sect - 1][0] == 'b':
                        moves.append(
                            Move((a, sect), (a-1, sect - 1), self.board))
                    

        else:  # black's turn
            # one-square pawn move
            if on_right_half:
                if self.board[a][sect + 1] == "--":
                    moves.append(Move((a, sect), (a, sect + 1), self.board))
                    # two-square pawn move
                    if sect == 5 and self.board[a][sect + 2] == "--":
                        moves.append(
                            Move((a, sect), (a, sect + 2), self.board))
            elif on_left_half_B:
                if self.board[a][sect - 1] == "--":
                    moves.append(Move((a, sect), (a, sect - 1), self.board))
                    # two square pawn move
                    if sect == 2 and self.board[a][sect - 2] == "--":
                        moves.append(
                            Move((a, sect), (a, sect - 2), self.board))
            elif sect == 0 and self.board[a][15] == "--":
                moves.append(Move((a, sect), (a, 15), self.board))

    def get_rook_moves(self, a, sect, moves):
        pass


class Move():
    ann_to_rank = {0: '1', 1: '2', 2: '3', 3: '4'}
    rank_to_ann = {v: k for k, v in ann_to_rank.items()}

    sect_to_file = {0: 'l', 1: 'k', 2: 'j', 3: 'i', 4: 'h', 5: 'g', 6: 'f', 7: 'e',
                    8: 'd', 9: 'c', 10: 'b', 11: 'a', 12: 'p', 13: 'o', 14: 'n', 15: 'm'}
    file_to_sect = {v: k for k, v in sect_to_file.items()}

    def __init__(self, start_space, end_space, board):
        self.start_ann = start_space[0]
        self.start_sect = start_space[1]

        self.end_ann = end_space[0]
        self.end_sect = end_space[1]

        self.piece_moved = board[self.start_ann][self.start_sect]
        self.piece_captured = board[self.end_ann][self.end_sect]

        self.move_id = self.start_ann * 1000 + self.start_sect * 100 + \
            self.end_ann * 10 + self.end_sect

        """
        Overriding the equals method
        """

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_file_rank(self.start_ann, self.start_sect) + self.get_file_rank(self.end_ann, self.end_sect)

    def get_file_rank(self, a, sect):
        return self.sect_to_file[sect] + self.ann_to_rank[a]
