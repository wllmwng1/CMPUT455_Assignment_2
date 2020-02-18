# Cmput 455 sample code
# Game basics - constants and definitions two player games
# Written by Martin Mueller

import random

# encoding of colors of points on the board
EMPTY = 0 
BLACK = 1 # Also used for 'X'
WHITE = 2 # Also used for 'O'

def isBlackWhite(color):
    return (color == BLACK) or (color == WHITE)
    
def isEmptyBlackWhite(color):
    return (color == EMPTY) or (color == BLACK) or (color == WHITE)

def opponent(color):
    assert isBlackWhite(color)
    return BLACK + WHITE - color

def colorAsString(color):
    assert isBlackWhite(color)
    if color == BLACK:
        return "Black"
    else:
        return "White"

def winnerAsString(color):
    assert isEmptyBlackWhite(color)
    if color == BLACK:
        return "Black"
    elif color == WHITE:
        return "White"
    else:
        return "Draw"

