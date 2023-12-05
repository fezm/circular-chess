import pygame as pg
from constants import *
from board import Board

FPS = 60
pg.init()
WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Circular Chess Board")

def main():
    run = True
    clock = pg.time.Clock()
    board = Board()
    board.draw_asects(WINDOW)
    
    while run:
        clock.tick(FPS)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            
            if event.type == pg.MOUSEBUTTONDOWN:
                pass
                
        pg.display.update()

    pg.quit()
    
main()