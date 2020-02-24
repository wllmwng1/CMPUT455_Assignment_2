from transposition_table import TranspositionTable
from nogo_board import NoGoBoard
from board_util import GoBoardUtil, coord_to_point
from gtp_connection import move_to_coord
from solve_nogo import solve
import cProfile

SIZE = 4
DEPTH = 10
TIMELIMIT = 70

def move_to_point(move):
    coord = move_to_coord(move, SIZE)
    return coord_to_point(coord[0], coord[1], SIZE)

def main():
    state = NoGoBoard(SIZE)
    tt = TranspositionTable(SIZE)

    cur = state.current_player
    opp = GoBoardUtil.opponent(cur)

    state.play_move(move_to_point("a4"), cur);
    state.play_move(move_to_point("a2"), opp);
    state.play_move(move_to_point("d1"), cur);
    state.play_move(move_to_point("d2"), opp);
    # state.play_move(move_to_point("d3"), cur);
    
    result = solve(state, tt, DEPTH, TIMELIMIT)

    print(str(result))

if __name__ == "__main__":
    cProfile.run("main()")
    # main()

