
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
        pass
    