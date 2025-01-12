import numpy as np
import pygame as pg
import pygame.gfxdraw
from move import Move
from pawn import Pawn
from constants import *


class Board:
    def __init__(self):
        # Board is a 4x16 2D list, each entry has 2 characters:
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
        self.move_functions = {'p': self.get_pawn_moves,
                               'R': self.get_rook_moves,
                               'B': self.get_bishop_moves,
                               'N': self.get_knight_moves,
                               'Q': self.get_queen_moves,
                               'K': self.get_king_moves}

        self.white_to_move = True

        self.move_log = []

    def reset(self):
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
        self.move_log = []
        self.white_to_move = True
        return

    def fill_arc(self, window, center, radius, theta0, theta1, color, ndiv=150):
        # Fills an arc in the window to represent a circular sector
        x0, y0 = center

        dtheta = (theta1 - theta0) / ndiv
        angles = [theta0 + i*dtheta for i in range(ndiv + 1)]

        points = [(x0, y0)] + [(x0 + radius * np.cos(theta), y0 -
                                radius * np.sin(theta)) for theta in angles]

        pygame.gfxdraw.filled_polygon(window, points, color)

    def draw_board(self, window):
        # Draws the circular chess board
        for ring in range(ANNULI):
            radius = WIDTH//2 - ring*SPACING
            for sector in range(SECTORS):
                color = DARK if ((sector+ring) % 2) else LIGHT

                self.fill_arc(window, CENTER, radius, sector *
                              SLICE, (sector+1)*SLICE, color)

        pg.draw.circle(window, GRAY, CENTER, MIDDLE_RADIUS)

    def draw_pieces(self, window, images):
        # Draws the chess pieces on the circular chess board

        # Get the center coordinates of the circular chess board
        x0, y0 = CENTER
        # Starting angle for the first sector
        theta0 = SLICE / 2
        # Initial radius of the circular board
        r0 = MIDDLE_RADIUS

        # Iterate over the annuli (circles) on the chess board
        for a in range(ANNULI):
            # Calculate the current radius, accounting for spacing and scaling
            r = r0 + (SPACING * a)
            r *= SCALING

            # Iterate over the sectors in each annulus
            for sect in range(SECTORS):
                # Get the chess piece at the current annulus and sector
                piece = self.board[a][sect]

                # Check if the square is not empty
                if piece != "--":
                    # Calculate the angle based on the sector
                    theta = theta0 + (SLICE * sect)

                    # Calculate the coordinates for placing the piece on the board
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

                    # Blit the chess piece image onto the window at the calculated coordinates
                    window.blit(images[piece], pg.Rect(
                        x, y, PIECE_SIZE, PIECE_SIZE))

    def draw(self, window, images):
        # Combines the board and piece drawing
        window.fill(GRAY)
        self.draw_board(window)
        self.draw_pieces(window, images)

    def make_move(self, move: Move) -> None:
        # Makes a move on the board and updates the game state
        self.board[move.start_ann][move.start_sect] = "--"
        self.board[move.end_ann][move.end_sect] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        return

    def undo_move(self) -> None:
        # Undoes the last move made
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_ann][move.start_sect] = move.piece_moved
            self.board[move.end_ann][move.end_sect] = move.piece_captured
            self.white_to_move = not self.white_to_move
        return

    def get_valid_moves(self) -> list:
        # TODO
        valid_moves = self.get_all_moves()
        # for move in valid_moves:
        #     # Do something
        return valid_moves

    def get_all_moves(self) -> list:
        # Gets all valid moves for the current player
        moves = []
        for a in range(ANNULI):
            for sect in range(SECTORS):
                turn = self.board[a][sect][0]
                if (turn == 'w' and self.white_to_move) or \
                        (turn == 'b' and not self.white_to_move):
                    piece = self.board[a][sect][1]
                    # Calls appropriate move function based on piece type
                    self.move_functions[piece](a, sect, moves)

        return moves

    def get_pawn_moves(self, a, sect, moves) -> None:

        color, enemy_color = ('w', 'b') if self.white_to_move else ('b', 'w')
        pawn = Pawn(sect, color)
        next_sect = (sect + pawn.dir) % SECTORS

        # 1-space pawn move
        if self.board[a][next_sect] == "--":
            moves.append(Move((a, sect), (a, next_sect), self.board))
            # 2-space pawn move
            next_next_sect = (next_sect + pawn.dir) % SECTORS
            if (pawn.sector == pawn.start_sector) and self.board[a][next_next_sect] == "--":
                moves.append(
                    Move((a, sect), (a, next_next_sect), self.board))

        # Captures
        if a - 1 >= 0:
            if self.board[a - 1][next_sect][0] == enemy_color:
                moves.append(Move((a, sect), (a - 1, next_sect), self.board))
        if a + 1 < 4:
            if self.board[a + 1][next_sect][0] == enemy_color:
                moves.append(Move((a, sect), (a + 1, next_sect), self.board))

        # Promotions: TODO
        return

    def get_rook_moves(self, a, sect, moves) -> None:
        # Determine the color of the enemy based on the current player's turn
        enemy_color = 'b' if self.white_to_move else 'w'

        # Define possible movement directions for a rook
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        def is_valid_space(ann, sec):
            # Check if the given coordinates are within the valid chess board range
            return (sec >= 0 and sec < 16) and (ann >= 0 and ann < 4)

        def check(direction, ann, sec):
            # Helper function to check and add moves in a given direction

            # Calculate the new coordinates based on the movement direction
            new_a = ann + direction[0]
            new_sect = sec + direction[1]

            # Handle wrap-around if the new sector goes beyond the board limits
            if new_sect == -1:
                new_sect = 15
            elif new_sect == 16:
                new_sect = 0

            # Check if the new coordinates are within the valid chess board range
            if not is_valid_space(new_a, new_sect):
                return

            # If the target space is empty, add a regular move and recursively check further
            if self.board[new_a][new_sect] == "--":
                moves.append(Move((a, sect), (new_a, new_sect), self.board))
                check(direction, new_a, new_sect)
                return
            # If the target space has an enemy piece, add a capturing move and stop
            elif self.board[new_a][new_sect][0] == enemy_color:
                moves.append(Move((a, sect), (new_a, new_sect), self.board))
                return
            else:
                # If the target space has a friendly piece, stop searching in this direction
                return

        # Iterate over all possible movement directions for a rook
        for d in directions:
            # Check and add moves in the specified direction
            check(d, a, sect)

    def get_bishop_moves(self, a, sect, moves) -> None:
        # Determine the color of the enemy based on the current player's turn
        enemy_color = 'b' if self.white_to_move else 'w'

        # Define possible movement directions for a bishop
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        def is_valid_space(ann, sec):
            # Check if the given coordinates are within the valid chess board range
            return (sec >= 0 and sec < 16) and (ann >= 0 and ann < 4)

        def check(direction, ann, sec):
            # Helper function to check and add moves in a given diagonal direction

            # Calculate the new coordinates based on the movement direction
            new_a = ann + direction[0]
            new_sect = sec + direction[1]

            # Handle wrap-around if the new sector goes beyond the board limits
            if new_sect == -1:
                new_sect = 15
            elif new_sect == 16:
                new_sect = 0

            # Check if the new coordinates are within the valid chess board range
            if not is_valid_space(new_a, new_sect):
                return

            # If the target space is empty, add a regular move and recursively check further
            if self.board[new_a][new_sect] == "--":
                moves.append(Move((a, sect), (new_a, new_sect), self.board))
                check(direction, new_a, new_sect)
                return
            # If the target space has an enemy piece, add a capturing move and stop
            elif self.board[new_a][new_sect][0] == enemy_color:
                moves.append(Move((a, sect), (new_a, new_sect), self.board))
                return
            else:
                # If the target space has a friendly piece, stop searching in this direction
                return

        # Iterate over all possible diagonal movement directions for a bishop
        for d in directions:
            # Check and add moves in the specified diagonal direction
            check(d, a, sect)

    def get_queen_moves(self, a, sect, moves) -> None:
        # Combine the moves of a bishop and a rook to get queen moves
        self.get_bishop_moves(a, sect, moves)
        self.get_rook_moves(a, sect, moves)
        return

    def get_king_moves(self, a, sect, moves):
        # Determine the opponent's color based on the current player's turn
        enemy_color = 'b' if self.white_to_move else 'w'

        # Define possible directions for king movement
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1),
                      (1, 0), (0, 1), (-1, 0), (0, -1)]

        def is_valid_space(ann, sec):
            # Helper function to check if a space is within the board boundaries
            return (sec >= 0 and sec < 16) and (ann >= 0 and ann < 4)

        def check(direction, ann, sec):
            # Helper function to check and add valid king moves in a given direction
            new_a = ann + direction[0]
            new_sect = sec + direction[1]
            if new_sect == -1:
                new_sect = 15
            elif new_sect == 16:
                new_sect = 0
            if not is_valid_space(new_a, new_sect):
                return

            if self.board[new_a][new_sect] == "--":
                # Empty space, valid king move
                moves.append(Move((a, sect), (new_a, new_sect), self.board))
            elif self.board[new_a][new_sect][0] == enemy_color:
                # Capturing opponent's piece, valid king move
                moves.append(Move((a, sect), (new_a, new_sect), self.board))

        # Check moves in all directions
        for d in directions:
            check(d, a, sect)

    def get_knight_moves(self, a, sect, moves):
        # Determine the opponent's color based on the current player's turn
        enemy_color = 'b' if self.white_to_move else 'w'

        # Define possible knight move directions
        directions = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                      (1, 2), (1, -2), (-1, 2), (-1, -2)]

        def is_valid_space(ann, sec):
            # Helper function to check if a space is within the board boundaries
            return (sec >= 0 and sec < 16) and (ann >= 0 and ann < 4)

        def check(direction, ann, sec):
            # Helper function to check and add valid knight moves in a given direction
            new_a = ann + direction[0]
            new_sect = sec + direction[1]

            # Adjust for circular board boundaries
            if new_sect == -1:
                new_sect = 15
            elif new_sect == 16:
                new_sect = 0
            elif new_sect == -2:
                new_sect = 14
            elif new_sect == 17:
                new_sect = 1

            if not is_valid_space(new_a, new_sect):
                return

            if self.board[new_a][new_sect] == "--":
                # Empty space, valid knight move
                moves.append(Move((a, sect), (new_a, new_sect), self.board))
            elif self.board[new_a][new_sect][0] == enemy_color:
                # Capturing opponent's piece, valid knight move
                moves.append(Move((a, sect), (new_a, new_sect), self.board))

        # Check moves in all directions
        for d in directions:
            check(d, a, sect)
