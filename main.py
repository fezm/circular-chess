import pygame as pg
from constants import *
from board import Board, Move
import numpy as np

FPS = 60

# move this later
IMAGES = {}


def load_images():
    pieces = ['wp', 'wN', 'wB', 'wR', 'wQ', 'wK',
              'bp', 'bN', 'bB', 'bR', 'bQ', 'bK']

    for piece in pieces:
        # IMAGES[piece] = pg.image.load("images/" + piece + ".png")
        # define width, height
        IMAGES[piece] = pg.transform.scale(pg.image.load(
            "images/" + piece + ".png"), (PIECE_SIZE, PIECE_SIZE))


def main():
    pg.init()

    WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Circular Chess Board")

    clock = pg.time.Clock()
    WINDOW.fill(GRAY)

    board = Board()
    valid_moves = board.get_valid_moves()
    move_made = False # variable for when a move is made
    
    load_images()
    # print(IMAGES.keys())

    run = True
    space_selected = () # keeps track of last click of the user (tuple: (annulus, sector))
    player_clicks = [] # keeps track of player clicks. array of tuples (list: [tuple])
    while run:
        # Process player inputs
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            
            # mouse handler
            elif event.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()  # (x, y) location of mouse
                x = location[0] - CENTER[0]
                y = CENTER[1] - location[1]
                
                a = int((np.sqrt(x**2 + y**2) - MIDDLE_RADIUS) // SPACING)
                sect = int((np.pi - np.arctan2(y,x)) // SLICE)
                
                if space_selected == (a, sect) or a < 0 or a > 3: # the user clicked the same space twice
                    space_selected = () # deselect
                    player_clicks = [] # clear clicks
                elif (board.board[a][sect] == "--" and not len(player_clicks)):
                    break
                else:
                    space_selected = (a, sect)
                    player_clicks.append(space_selected)
                    
                if len(player_clicks) == 2: # after second move
                    move = Move(player_clicks[0], player_clicks[1], board.board)
                    if move in valid_moves:
                        board.make_move(move)
                        print(move.get_chess_notation())
                        move_made = True
                    space_selected = ()
                    player_clicks = []
                
            # key handler
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    board.undo_move()
                    move_made = True


        clock.tick(FPS)

        # Logical udates here
        if move_made:
            valid_moves = board.get_valid_moves()
            move_made = False

        # Render the graphics here.
        board.draw_board(WINDOW)
        board.draw_pieces(WINDOW, IMAGES)
        pg.display.update()

    pg.quit()


if __name__ == "__main__":
    main()