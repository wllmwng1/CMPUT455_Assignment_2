# Cmput 455 sample code
# TicTacToe game board, rules, and a random game simulator
# For Lecture 10: added the code() method to compute a code for 
# use in a transposition table
# Written by Martin Mueller

import random
from game_basics import EMPTY, BLACK, WHITE, isEmptyBlackWhite, opponent

class TicTacToe(object):
# Board is stored in array of size 9 as follows:
# 0 1 2
# 3 4 5
# 6 7 8

    def __init__(self):
        self.resetGame()

    def resetGame(self):
        self.board = [EMPTY] * 9
        self.toPlay = BLACK
        self.moves = []
        self.drawWinner = EMPTY

    def resetToMoveNumber(self, moveNr):
        numUndos = self.moveNumber() - moveNr
        assert numUndos >= 0
        for _ in range(numUndos):
            self.undoMove()
        assert self.moveNumber() == moveNr

    def switchToPlay(self):
        self.toPlay = opponent(self.toPlay)

    def play(self, location):
        assert not self.endOfGame()
        assert self.board[location] == EMPTY
        self.board[location] = self.toPlay
        self.moves.append(location)
        self.switchToPlay()

    def undoMove(self):
        location = self.moves.pop()
        self.board[location] = EMPTY
        self.switchToPlay()
    
    def hasRow(self, color, start):
        return (    self.board[start] == color
                and self.board[start+1] == color
                and self.board[start+2] == color)

    def hasCol(self, color, start):
        return (    self.board[start] == color
                and self.board[start+3] == color
                and self.board[start+6] == color)
    
    def diag1(self, color):
        return (    self.board[0] == color
                and self.board[4] == color
                and self.board[8] == color)

    def diag2(self, color):
        return (    self.board[2] == color
                and self.board[4] == color
                and self.board[6] == color)
    
    def isWinner(self, color):
        return (   self.hasRow(color, 0)
                or self.hasRow(color, 3)
                or self.hasRow(color, 6)
                or self.hasCol(color, 0)
                or self.hasCol(color, 1)
                or self.hasCol(color, 2)
                or self.diag1(color)
                or self.diag2(color)
               )

    def winner(self):
        if self.isWinner(BLACK):
            return BLACK
        if self.isWinner(WHITE):
            return WHITE
        return EMPTY

    def setDrawWinner(self, color):
        assert isEmptyBlackWhite(color)
        self.drawWinner = color

    def staticallyEvaluateForToPlay(self):
        winColor = self.winner()
        if (winColor == EMPTY) and (self.drawWinner != EMPTY):
            winColor = self.drawWinner
        if winColor == self.toPlay:
            return True
        assert winColor == opponent(self.toPlay)
        return False
    
    def moveNumber(self):
        return len(self.moves)

    def endOfGame(self):
        return (   len(self.moves) == 9
                or self.winner() != EMPTY
               )

    def legalMoves(self):
        assert not self.endOfGame()
        moves = []
        for i in range(9):
            if self.board[i] == EMPTY:
                moves.append(i)
        return moves
        
    def code(self):
        c = 0
        for i in range(9):
            c = 3*c + self.board[i]
        return c

    # simulate one game from the current state until the end
    def simulate(self):
        i = 0
        if not self.endOfGame():
            allMoves = self.legalMoves()
            random.shuffle(allMoves)
            while not self.endOfGame():
                self.play(allMoves[i])
                i += 1
        return self.winner(), i

    def print(self):
        print(self.board[0:3])
        print(self.board[3:6])
        print(self.board[6:9])
