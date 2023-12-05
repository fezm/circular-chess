from math import pi, cos, sin
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

        points = [(x0, y0)] + [(x0 + radius * cos(theta), y0 -
                                radius * sin(theta)) for theta in angles]

        pygame.gfxdraw.filled_polygon(window, points, color)

    def draw_asects(self, window):
        window.fill(GRAY)
        # self.fill_arc(window, CENTER, WIDTH//2, 0, pi, RED)
        # self.fill_arc(window, CENTER, WIDTH//2, pi, 2*pi, BLUE)
        slice = 2*pi/SECTORS
        cc_rad = WIDTH//10
        spacing = (WIDTH//2 - cc_rad) // 4
        for ring in range(ANNULI):
            radius = WIDTH//2 - ring*spacing
            for sector in range(SECTORS):
                # color = LIGHT
                # if (sector+ring) % 2 != 0:
                #     color = DARK
                color = DARK if ((sector+ring) % 2) else LIGHT
                
                self.fill_arc(window, CENTER, radius, sector *
                              slice, (sector+1)*slice, color)
                
        pg.draw.circle(window, GRAY, CENTER, cc_rad)
