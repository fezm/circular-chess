import pygame as pg
from constants import *


class Piece:
    
    def __init__(self, ann, sect, color):
        self.ann = ann
        self.sect = sect
        self.color = color
        self.selected = False
        self.move_list = []
        self.king = False
        self.pawn = False
        
    def is_selected(self):
        return self.selected
    
    def update_valid_moves(self, board):
        pass
    
    def draw(self, win, color):
        pass
    
    def change_pos(self, pos):
        pass
    


class Bishop(Piece):
    # img = 0 ?
    
    def valid_moves(self, board):
        pass
    
    
class King(Piece):
    # img = 1 ?
    
    def valid_moves(self, board):
        pass
    
    
class Knight(Piece):
    # img = 2 ?
    
    def valid_moves(self, board):
        pass
    
    
class Pawn(Piece):
    # img = 3 ?
    
    def valid_moves(self, board):
        pass
    
    
class Queen(Piece):
    # img = 4 ?
    
    def valid_moves(self, board):
        pass
    

class Rook(Piece):
    # img = 5 ?
    
    def valid_moves(self, board):
        pass
    
