import numpy as np
import events as e

class LinkedGridNode:
    def __init__(self, u, l, pos):
        self.up = u
        self.left = l
        if u:
            self.up.down = self
        if l:
            self.left.right = self
        self.down = None
        self.right = None
        self.color = None
        self.x = pos[0]
        self.y = pos[1]
        self.pos = pos
    def colorize(self, c):
        self.color = c

class LinkedGrid:
    def __init__(self, width, height):
        self.matrix = []
        for w in range(width):
            self.matrix.append([])
            for h in range(height):
                if h != 0:
                    nodeUp = self.matrix[w][h-1]
                else:
                    nodeUp = None
                if w!= 0:
                    nodeLeft = self.matrix[w-1][h]
                else:
                    nodeLeft = None
                pos = (w,h)
                self.matrix[w].append(LinkedGridNode(nodeUp,nodeLeft,pos))

class Piece:
    def __init__(self, matrix, player):
        self.player = player
        self.c = player.c
        self.m = np.array(matrix)
    def fixPos(self):
        #add player position to piece array dimensions
        botright = self.player.pos + self.m.shape
        #check if this goes off the board...
        while botright[0] > 20:#hardcoding size for now, fix for variable board size
            self.player.pos -= (1,0)
            botright -= (1,0)
        while botright[1] > 20:
            self.player.pos -= (0,1)
            botright -= (0,1)
    def rotflip(self,rottype):
        print(self.m)
        if rottype == "rotCW":
            self.m = np.rot90(self.m,3)
        elif rottype == "rotCCW":
            self.m = np.rot90(self.m)
        elif rottype == "flip":
            self.m = np.fliplr(self.m)
        print(rottype)
        print(self.m)
        self.fixPos()
    def move(self, direction):
        if direction == "up":
            self.player.pos -= (0,1)
        elif direction == "down":
            self.player.pos += (0,1)
        elif direction == "left":
            self.player.pos -= (1,0)
        elif direction == "right":
            self.player.pos += (1,0)
        self.fixPos()
        while self.player.pos[0] < 0:
            self.player.pos += (1,0)
        while self.player.pos[1] < 0:
            self.player.pos += (0,1)
    def place(self):
        bpos = board.matrix[self.player.pos[0]][self.player.pos[1]]
        for r in range(len(self.m)):
            for c in range(len(self.m[r])):
                if self.m[r][c] == 1:
                    board.matrix[r+bpos.x][c+bpos.y].colorize(self.c)
        self.player.delPiece()
                

class Player:
    def __init__(self, color):
        self.c = color
        self.pieces = dict()
        self.score = 0
        self.pos = np.array([0,0])
        with open("pieces.blok", "r") as f:
            for line in f:
                l = eval(line.rstrip())
                if isinstance(l,int):
                    s = l
                    if s not in self.pieces:
                        self.pieces[s] = []
                elif isinstance(l,list):
                    l = Piece(l, self)
                    self.pieces[s].append(l)
                    self.score -= s
        self.curPiece = self.pieces[1][0]
        self.curPieceIndex = 0
        self.curPieceKey = 1
    def setPos(self, pos):
        self.pos = pos
    def getPiece(self, num):
        if num in self.pieces:
            if self.pieces[num]:
                self.curPiece = self.pieces[num][0]
                self.curPieceKey = num
                self.curPieceIndex = 0
            else:
                self.curPieceKey = next(iter(self.pieces))
                self.curPieceIndex = 0
                self.curPiece = self.pieces[self.curPieceKey][0]
        else:
            self.curPieceKey = next(iter(self.pieces))
            self.curPieceIndex = 0
            self.curPiece = self.pieces[self.curPieceKey][0]
        self.curPiece.fixPos()
    def nextPiece(self, direction):
        pKey = self.curPieceKey
        if direction == "f":
            self.curPieceIndex += 1
            if self.curPieceIndex >= len(self.pieces[pKey]):
                self.curPieceIndex = 0
        if direction == "b":
            self.curPieceIndex -= 1
            if self.curPieceIndex < 0:
                self.curPieceIndex = len(self.pieces[pKey])-1
        self.curPiece = self.pieces[pKey][self.curPieceIndex]
        self.curPiece.fixPos()
    def delPiece(self):
        pKey = self.curPieceKey
        pIn = self.curPieceIndex
        del self.pieces[pKey][pIn]
        if self.pieces[pKey]:
            self.nextPiece("b")
        else:
            del self.pieces[pKey]
            self.getPiece(1)
        

class Players:
    def __init__(self, ps, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        colors = ["r","g","b","y"]
        self.players = []
        for p in range(ps):
            self.players.append(Player(colors[p]))
        self.curI = 0
        self.cur = self.players[self.curI]
    def Notify(self, event):
        if isinstance(event, e.NextTurn):
            self.curI += 1
            if self.curI >= len(self.players):
                self.curI = 0
            self.cur = self.players[self.curI]
        elif isinstance(event, e.GetPiece):
            self.cur.getPiece(event.num)
        elif isinstance(event, e.NextPiece):
            self.cur.nextPiece(event.dir)
        elif isinstance(event, e.RotPiece):
            self.cur.curPiece.rotflip(event.rottype)
        elif isinstance(event, e.MovePiece):
            self.cur.curPiece.move(event.dir)
        elif isinstance(event, e.PlacePiece):
            if self.cur.curPiece.place():
                self.evManager.Post(e.NextTurn())
            

def createBoard(w=20,h=20, c=20):
    global board
    board = LinkedGrid(w,h)
def createPlayers(num, evManager):
    global players
    players = Players(num, evManager)
