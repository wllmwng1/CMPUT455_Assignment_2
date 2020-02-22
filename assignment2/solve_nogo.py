from nogo_board import NoGoBoard
from board_util import GoBoardUtil, \
                        BLACK, WHITE, EMPTY
from transposition_table import TranspositionTable
from negamax_tt import timed_negamax, timed_negamax_with_moves
import time

def call_search(state, timelimit):
    tt = TranspositionTable(state.size)
    result = None
    
    try:
        result = timed_negamax(state, tt, timelimit)
    except TimeoutError:
        result = None
    
    return result


def solve(state, timelimit):
    tt = TranspositionTable(state.size)
    
    result = None
    try:
        result = timed_negamax_with_moves(state.copy(), tt, timelimit)
    except TimeoutError:
        result = None
    
    return result


def solve_no_go():
    print("Solving NoGo")
    state = NoGoBoard(4)

    result = solve(state, 1)

    return

if __name__ == "__main__":
    print("testing solve_nogo.py...")
    solve_no_go()
