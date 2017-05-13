from pygame import display, Surface, font, image
import events as e
import objects as o
from numpy import array

class PygameView:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.window = display.set_mode((1400,800))
        self.winsize = self.window.get_size()
        display.set_caption("Blokus")
        self.background = Surface( self.window.get_size() )
        self.background.fill( (255,255,255) )
        self.window.blit( self.background, (0,0) )
        display.flip()
    def drawBoard(self):
        space = image.load("sprites\space.png")
        piece = image.load("sprites\piece.png")
        for row in o.board.matrix:
            for cell in row:
                self.window.blit(space,(cell.x*20,cell.y*20))
                if cell.color:
                    self.window.blit(piece,(cell.x*20+1,cell.y*20+1))
    def drawPiece(self):
        piece = image.load("sprites\piece.png")
        p = o.players.cur
        bpos = array((p.pos[0]*20+1, p.pos[1]*20+1))
        for r in range(len(p.curPiece.m)):
            for c in range(len(p.curPiece.m[0])):
                if p.curPiece.m[r][c] == 1:
                    pos = array((r*20,c*20))
                    self.window.blit(piece, bpos+pos)
    def Notify(self, event):
        if isinstance(event, e.TickEvent):
            self.drawBoard()
            self.drawPiece()
            display.update()
