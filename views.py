import events as e
import objects as o
import numpy as n
from pygame import display, Surface, font, image, surfarray

class PygameView:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.window = display.set_mode((500,400))
        self.winsize = self.window.get_size()
        display.set_caption("Blokus")
        self.background = Surface( self.window.get_size() )
        self.background.fill( (255,255,255) )
        self.window.blit( self.background, (0,0) )
        sbLoc = (len(o.board.matrix)*20+5, 0)
        self.scorebox = {"surf": Surface((100,200)), "loc": sbLoc }
        self.scorebox["surf"].fill((255,255,255))
        self.font = font.Font(None, 40)
        display.flip()
    def drawBoard(self):
        space = image.load("sprites\space.png")
        pieceImg = image.load("sprites\piece.png")
        pieceArray = surfarray.array3d(pieceImg)
        for row in o.board.matrix:
            for cell in row:
                self.window.blit(space,(cell.x*20,cell.y*20))
                if cell.color:
                    piece = n.array(pieceArray)
                    if cell.color == "r":
                        piece[:,:,1:] = 0
                    elif cell.color == "g":
                        piece[:,:,[0,2]] = 0
                    elif cell.color == "b":
                        piece[:,:,:2] = 0
                    elif cell.color == "y":
                        piece[:,:,2] = 0
                    surfarray.blit_array(pieceImg, piece)
                    self.window.blit(pieceImg,(cell.x*20+1,cell.y*20+1))
    def drawPiece(self):
        pieceImg = image.load("sprites\piece.png")
        p = o.players.cur
        pieceArray = surfarray.array3d(pieceImg)
        if p.c == "r":
            pieceArray[:,:,1:] = 0
        elif p.c == "g":
            pieceArray[:,:,[0,2]] = 0
        elif p.c == "b":
            pieceArray[:,:,:2] = 0
        elif p.c == "y":
            pieceArray[:,:,2] = 0
        surfarray.blit_array(pieceImg, pieceArray)
        bpos = n.array((p.pos[0]*20+1, p.pos[1]*20+1))
        for r in range(len(p.curPiece.m)):
            for c in range(len(p.curPiece.m[0])):
                if p.curPiece.m[r][c] == 1:
                    pos = n.array((c*20,r*20))
                    self.window.blit(pieceImg, bpos+pos)
    def drawScores(self):
        self.scorebox["surf"].fill((255,255,255))
        scores = []
        for player in o.players.players:
            scores.append(self.font.render(player.c+": "+str(player.score), True, (0,0,0)))
        for s in range(len(scores)):
             self.scorebox["surf"].blit(scores[s],(0,s*50))
        self.window.blit(self.scorebox["surf"],self.scorebox["loc"])
    def Notify(self, event):
        if isinstance(event, e.TickEvent):
            self.drawBoard()
            self.drawPiece()
            self.drawScores()
            display.update()
