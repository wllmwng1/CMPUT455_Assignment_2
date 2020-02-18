from nogo_board import NoGoBoard
from board_util import GoBoardUtil, \
                        BLACK, WHITE, EMPTY
from gtp_connection import TranspositionTable
from negamax_tt import negamax, timed_negamax
import time

def call_search(state, timelimit=10):
    tt = TranspositionTable()
    return timed_negamax(state, tt, timelimit)


def solve(state):
    result = call_search(state, 1)
    return result



def solve_no_go():
    print("Solving NoGo")
    state = NoGoBoard(7)

    result = solve(state)

    print("result is: {}".format(result))

    return

if __name__ == "__main__":
    print("testing solve_nogo.py...")
    solve_no_go()


