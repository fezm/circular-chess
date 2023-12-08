from math import cos, sin
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

        self.selected_piece = None

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
            for sect in range(SECTORS):
                piece = self.board[a][sect]
                if piece != "--":

                    theta = theta0 + (SLICE * sect)

                    if sect >= 0 and sect < 4:
                        quad = "top left"
                        x = x0 + ((r * np.cos(pi - theta))) - (PIECE_SIZE/2)
                        y = y0 - ((r * np.sin(pi - theta))) - PIECE_SIZE
                    elif sect >= 4 and sect < 8:
                        quad = "top right"
                        x = x0 - (r * np.cos(theta)) - (PIECE_SIZE/2)
                        y = y0 - (r * np.sin(theta)) - PIECE_SIZE
                    elif sect >= 8 and sect < 12:
                        quad = "bottom right"
                        x = x0 + (r * np.cos(pi - theta)) - (PIECE_SIZE/2)
                        y = y0 - (r * np.sin(pi - theta))
                    elif sect >= 12 and sect < 16:
                        quad = "bottom left"
                        x = x0 + (r * np.cos(pi - theta)) - (PIECE_SIZE/2)
                        y = y0 - (r * np.sin(pi - theta))

                    window.blit(images[piece], pg.Rect(
                        x, y, PIECE_SIZE, PIECE_SIZE))

    def draw(self, window, images):
        self.draw_board(window)
        self.draw_pieces(window, images)
