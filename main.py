#Blokus in Pygame by Beatrice Evelyn Corfman, started 05/12/2017
#The most recent version of this can be found at:
#https://github.com/notthatstraight/blokus

#MVC framework adapted from http://ezide.com/games/writing-games.html

import sys
import pygame
import events as e
import controllers as c
import views as v
import objects as o

def init(evManager):
    o.createBoard()
    o.createPlayers(4,evManager)
    print("\nRules:")
    print("Your first piece must be placed in a corner.")
    print("For a two player game, this is restricted to the top-left and bottom-right")
    print("All pieces after that must be placed diagonally adjacent to one of your other pieces.")
    print("You cannot place a piece directly adjacent to any of your other pieces, or overlapping any piece.")
    print("Your score is based on the total number of tiles in the pieces you haven't played.")
    print("This version of the game does not give you a bonus for playing the 1-tile last.")
    print("\nControls:")
    print("Place a piece: Enter")
    print("Move a piece: arrow keys")
    print("Rotate piece clockwise: x")
    print("Rotate piece counterclockwise: z")
    print("Flip piece: left shift")
    print("Go to previous/next piece of current size: </> or ,/.")
    print("Change to pieces of size [#]: #")
    print("Resign/declare no moves remaining: escape")
    print("\nThere's currently no end-game detection, and resignation uses this terminal to confirm.")
    print("Fixes to those will come in a later version, as will much more polish.")
    print("For now, thank you for playing this very rough version! Any bug reports would be appreciated.")
    print("https://github.com/notthatstraight/blokus/issues")
    input("Press enter when you're ready to play!")

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
