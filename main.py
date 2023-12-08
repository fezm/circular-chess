import pygame as pg
from constants import *
from board import Board
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


# move this later
"""
Responsible for drawing the pieces. Move this into board
"""


def draw_game_state(window, gs):
    # drawBoard, pretty much our draw_board
    # drawPieces
    pass


def main():
    pg.init()

    WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Circular Chess Board")

    clock = pg.time.Clock()
    WINDOW.fill(GRAY)

    board = Board()
    load_images()
    # print(IMAGES.keys())

    board.draw_board(WINDOW)  # move this later ?
    board.draw_pieces(WINDOW, IMAGES)

    run = True
    while run:
        # Process player inputs
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            elif event.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()  # (x, y) location of mouse
                x = location[0] - CENTER[0]
                y = CENTER[1] - location[1]
                
                a = int((np.sqrt(x**2 + y**2) - MIDDLE_RADIUS) // SPACING)
                sect = int((np.pi - np.arctan2(y,x)) // SLICE)
                
                if a < 0 or a > 3:
                    break
                print(f"piece: {board.board[a][sect]}")
                pass

        clock.tick(FPS)  # move this later ?

        # Logical udates here

        # Render the graphics here.
        pg.display.update()

    pg.quit()


if __name__ == "__main__":
    main()
