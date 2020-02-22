from nogo_board import NoGoBoard
from board_util import GoBoardUtil, \
                        BLACK, WHITE, EMPTY
from transposition_table import TranspositionTable
from timeout_exception import TimeoutException
from negamax_tt import timed_negamax, timed_negamax_with_moves
import time

def call_search(state, timelimit):
    tt = TranspositionTable(state.size)
    result = None

    try:
        result = timed_negamax(state, tt, timelimit)
    except TimeoutException:
        result = None

    return result


def solve(state, tt=None, timelimit=10):
    if (tt == None):
        tt = TranspositionTable(state.size)

    result = None
    try:
        result = timed_negamax_with_moves(state.copy(), tt, timelimit)
    except TimeoutException:
        result = None

    return result


def solve_no_go():
    print("Solving NoGo")
    state = NoGoBoard(3)

    result = solve(state, None, 1)
    print(result)

    return

if __name__ == "__main__":
    print("testing solve_nogo.py...")
    solve_no_go()
