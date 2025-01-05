import pygame as pg
from constants import *
from board import Board
from move import Move
import numpy as np

FPS = 60

# Move this later
IMAGES = {}


def load_images():
    pieces = ['wp', 'wN', 'wB', 'wR', 'wQ', 'wK',
              'bp', 'bN', 'bB', 'bR', 'bQ', 'bK']

    for piece in pieces:
        # Load and scale images
        IMAGES[piece] = pg.transform.scale(pg.image.load(
            "images/" + piece + ".png"), (PIECE_SIZE, PIECE_SIZE))


def main():
    pg.init()

    # Set up the game window
    WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Circular Chess Board")

    clock = pg.time.Clock()
    WINDOW.fill(GRAY)

    # Initialize the chess board
    board = Board()
    valid_moves = board.get_valid_moves()
    move_made = False  # Variable for when a move is made

    # Load chess piece images
    load_images()

    run = True
    space_selected = ()  # Keeps track of the last click of the user (tuple: (annulus, sector))
    # Keeps track of player clicks. Array of tuples (list: [tuple])
    player_clicks = []

    while run:
        """
        Process player inputs
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break

            # Mouse handler
            elif event.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()  # (x, y) location of the mouse
                x = location[0] - CENTER_X
                y = CENTER_Y - location[1]

                a = int((np.sqrt(x**2 + y**2) - MIDDLE_RADIUS) // SPACING)
                sect = int((np.pi - np.arctan2(y, x)) // SLICE)

                if space_selected == (a, sect) or a < 0 or a > 3:
                    # The user clicked the same space twice or clicked outside of the board
                    space_selected = ()  # Deselect
                    player_clicks = []  # Clear clicks
                elif (board.board[a][sect] == "--" and not len(player_clicks)):
                    break
                else:
                    space_selected = (a, sect)
                    player_clicks.append(space_selected)

                if len(player_clicks) == 2:  # After the second move
                    move = Move(player_clicks[0],
                                player_clicks[1], board.board)
                    if move in valid_moves:
                        board.make_move(move)
                        print(move.get_chess_notation())
                        move_made = True
                    space_selected = ()
                    player_clicks = []

            # Key handler
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    board.undo_move()
                    move_made = True

        
        """
        Logical updates
        """
        clock.tick(FPS)
        if move_made:
            valid_moves = board.get_valid_moves()
            move_made = False

        """
        Render graphics
        """
        board.draw(WINDOW, IMAGES)
        pg.display.update()

    pg.quit()


if __name__ == "__main__":
    main()
