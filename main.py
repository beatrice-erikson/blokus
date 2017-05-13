import sys
import pygame
import events as e
import controllers as c
import views as v
import objects as o

def init(evManager):
    o.createBoard()
    o.createPlayers(1,evManager)
    

def main():
    pygame.init()
    evManager = e.EventManager()
    keyb = c.KeyboardController(evManager)
    tick = c.TickController(evManager)
    init(evManager)
    pygameView = v.PygameView(evManager)

    tick.run()
    pygame.quit()
    sys.exit()

main()
