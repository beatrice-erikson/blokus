import pygame
from pygame.key import *
import events as e



class KeyboardController:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
    def Notify(self, event):
        if isinstance(event, e.TickEvent):
            for event in pygame.event.get():
                ev = None
                if event.type == pygame.QUIT:
                    ev = e.QuitEvent()
                if event.type == pygame.KEYDOWN:
                    if event.key in { pygame.K_1, pygame.K_KP2 }:
                        ev = e.GetPiece(1)
                    elif event.key in { pygame.K_2, pygame.K_KP2 }:
                        ev = e.GetPiece(2)
                    elif event.key in { pygame.K_3, pygame.K_KP3 }:
                        ev = e.GetPiece(3)
                    elif event.key in { pygame.K_4, pygame.K_KP4 }:
                        ev = e.GetPiece(4)
                    elif event.key in { pygame.K_5, pygame.K_KP5 }:
                        ev = e.GetPiece(5)
                    elif event.key == pygame.K_z:
                        ev = e.RotPiece("rotCCW")
                    elif event.key == pygame.K_x:
                        ev = e.RotPiece("rotCW")
                    elif event.key == pygame.K_LSHIFT:
                        ev = e.RotPiece("flip")
                    elif event.key in { pygame.K_COMMA, pygame.K_LESS }:
                        ev = e.NextPiece("b")
                    elif event.key in { pygame.K_PERIOD, pygame.K_GREATER }:
                        ev = e.NextPiece("f")
                    elif event.key == pygame.K_UP:
                        ev = e.MovePiece("up")
                    elif event.key == pygame.K_DOWN:
                        ev = e.MovePiece("down")
                    elif event.key == pygame.K_LEFT:
                        ev = e.MovePiece("left")
                    elif event.key == pygame.K_RIGHT:
                        ev = e.MovePiece("right")
                    elif event.key == { pygame.K_KP_ENTER, pygame.K_RETURN }:
                        ev = e.PlacePiece()
                    elif event.key == pygame.K_ESCAPE:
                        ev = e.ResignEvent()
                if ev:
                    self.evManager.Post(ev)

class TickController:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.on = True

    def run(self):
        while self.on:
            self.evManager.Post(e.TickEvent())
    def Notify(self, event):
        if isinstance(event, e.QuitEvent):
            self.on = False
