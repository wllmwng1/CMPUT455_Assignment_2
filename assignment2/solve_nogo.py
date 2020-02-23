from nogo_board import NoGoBoard
from board_util import GoBoardUtil, \
                        BLACK, WHITE, EMPTY
from transposition_table import TranspositionTable
from timeout_exception import TimeoutException
from negamax_tt import timed_negamax, timed_negamax_with_moves, timed_alphabeta_negamax
import time
import cProfile

def call_search(state, timelimit):
    tt = TranspositionTable(state.size)
    result = None

    try:
        result = timed_negamax(state, tt, timelimit)
    except TimeoutException:
        result = None

    return result


def solve(state, tt=None, depth=1000, timelimit=10):
    if (tt == None):
        tt = TranspositionTable(state.size)

    result = None
    try:
        result = timed_negamax_with_moves(state.copy(), tt, depth, timelimit)
    except TimeoutException:
        result = None

    return result


def solve_no_go():
    print("Solving NoGo")
    state = NoGoBoard(4)

    result = solve(state, None, 100)
    print(result)

    return

if __name__ == "__main__":
    print("testing solve_nogo.py...")
    cProfile.run("solve_no_go()")
