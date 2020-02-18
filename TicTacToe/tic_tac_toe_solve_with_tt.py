# Cmput 455 sample code
# Boolean Negamax for TicTacToe, with transposition table
# Written by Martin Mueller

from game_basics import EMPTY, BLACK, WHITE, opponent, winnerAsString
from tic_tac_toe import TicTacToe
from transposition_table_simple import TranspositionTable
from boolean_negamax_tt import negamaxBoolean
import time

def call_search(state):
    tt = TranspositionTable() # use separate table for each color
    return negamaxBoolean(state, tt)

def solve(state): 
    state.setDrawWinner(opponent(state.toPlay))
    win = call_search(state)
    if win:
        return state.toPlay
    # loss or draw, do second search to find out
    state.setDrawWinner(state.toPlay)
    if call_search(state):
        return EMPTY # draw
    else: # loss
        return opponent(state.toPlay)

def test_solve_with_tt():
    t = TicTacToe()
    start = time.process_time()
    result = solve(t)
    time_used = time.process_time() - start
    print("Result: {}\nTime used: {:.4f}".format(
        winnerAsString(result), time_used))

test_solve_with_tt()
