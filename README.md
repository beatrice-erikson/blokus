# blokus

blokus in pygame because why not  
##

Rules:
Your first piece must be placed in a corner. 
For a two player game, this is restricted to the top-left and bottom-right

All pieces after that must be placed diagonally adjacent to one of your other pieces.
  
You cannot place a piece directly adjacent to any of your other pieces, or overlapping any piece.

Your score is based on the total number of tiles in the pieces you haven't played.  

This version of the game does not give you a bonus for playing the 1-tile last.

  
##Controls:

Place a piece: Enter, or click on top-left of piece on board (sort of)  

Move a piece: arrow keys  

Rotate piece clockwise: x  

Rotate piece counterclockwise: z
  
Flip piece: left shift  

Go to previous/next piece of current size: </> or ,/.
  
Change to pieces of size [#]: #
  
Resign/declare no moves remaining: escape  


  
There's currently no end-game detection, and resignation uses this terminal to confirm. 
Fixes to those will come in a later version, as will much more polish.
 For now, thank you for playing this very rough version! Any bug reports would be appreciated.
https://github.com/notthatstraight/blokus/issues

  
  
Extra note on mouse piece placement: The way this actually works currently is that, if you click in such a way that the game tries to move your piece (so, anywhere on the board), and after trying to move your piece, the piece winds up in the same place, the game then attempts to place it.
This is based on player position, which is the top-left of a rectangular bounding box on the piece.