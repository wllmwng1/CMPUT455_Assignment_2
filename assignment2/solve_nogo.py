from nogo_board import NoGoBoard
from board_util import GoBoardUtil, \
                        BLACK, WHITE, EMPTY
from gtp_connection import TranspositionTable
from negamax_tt import negamax

def call_search(state):
    tt = TranspositionTable()
    return negamax(state, tt)


def solve(state):

    current_player = state.current_player

    result = call_search(state)

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


