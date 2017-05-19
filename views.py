import events as e
import objects as o
import numpy as n
from pygame import display, Surface, font, image, surfarray
from os.path import join

class PygameView:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.window = display.set_mode((700,420))
        self.winsize = self.window.get_size()
        display.set_caption("Blokus")
        self.background = Surface( self.window.get_size() )
        self.background.fill( (255,255,255) )
        self.window.blit( self.background, (0,0) )
        sbLoc = (len(o.board.matrix)*20+5, 0)
        self.scorebox = {"surf": Surface((100,200)), "loc": sbLoc }
        self.scorebox["surf"].fill((255,255,255))
        self.font = font.Font(None, 40)
        pbLoc = (sbLoc[0] + 100, 0)
        self.piecebox = {"surf": Surface((200,420)), "loc": pbLoc }
        self.piecebox["surf"].fill((255,255,255))
        self.drawBoard()
        self.drawScores()
        self.drawPlayerPieces()
        display.flip()
    def drawBoard(self):
        space = image.load(join("sprites", "space.png"))
        pieceImg = image.load(join("sprites", "piece.jpg"))
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
        pieceImg = image.load(join("sprites", "piece.jpg"))
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
        pieceImg.set_alpha(175)
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
    def drawPlayerPieces(self):
        self.piecebox["surf"].fill((255,255,255))
        pieceImg = image.load(join("sprites", "piecesmall.jpg"))
        
        pieceArrays = {"r": surfarray.array3d(pieceImg),
                       "g": surfarray.array3d(pieceImg),
                       "b": surfarray.array3d(pieceImg),
                       "y": surfarray.array3d(pieceImg)}
        pieceArrays["r"][:,:,1:] = 0
        pieceArrays["g"][:,:,[0,2]] = 0
        pieceArrays["b"][:,:,:2] = 0
        pieceArrays["y"][:,:,2] = 0

        bpos = n.array((0,0))
        for player in o.players.players:
            surfarray.blit_array(pieceImg, pieceArrays[player.c])
            for size in player.pieces.keys():
                for p in player.pieces[size]:
                    if len(p.m) < len(p.m[0]):
                        isTaller = True
                        h = len(p.m)
                    else:
                        isTaller = False
                        h = len(p.m[0])
                    for r in range(len(p.m)):
                        for c in range(len(p.m[0])):
                            if isTaller:
                                x = c
                                y = r
                            else:
                                x = r
                                y = c
                            if p.m[r][c] == 1:
                                pos = n.array((x*9,y*9))
                                self.piecebox["surf"].blit(pieceImg, bpos+pos)
                    bpos[1] += h*9 + 1
            bpos[0] += 50
            bpos[1] = 0
        self.window.blit(self.piecebox["surf"],self.piecebox["loc"])
    def Notify(self, event):
        if isinstance(event, e.TickEvent):
            self.drawBoard()
            self.drawPiece()
            display.update()
        if isinstance(event, e.NextTurn):   #none of these change within a turn
            self.drawScores()
            self.drawPlayerPieces()
            display.update()
