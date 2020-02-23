from nogo_board import NoGoBoard
from board_util import GoBoardUtil, \
                        BLACK, WHITE, EMPTY
from transposition_table import TranspositionTable
from timeout_exception import TimeoutException
import time
import signal
from random import randint


def immediately_evaluate(signum, frame):
    raise TimeoutException("TIMELIMIT ERROR: timed out");


def store_result(tt, state, result):
    tt.store(state.code(tt), result)
    return result


def switch_toPlay(state):
    curr_player = state.current_player
    next_player = EMPTY

    if (curr_player == BLACK):
        next_player = WHITE
    elif (curr_player == WHITE):
        next_player = BLACK

    state.current_player = next_player
    return


def negamax(state, tt, depth):
    result = tt.lookup(state.code(tt))
    if result != None:
        return result
    if (state.is_game_ended() or depth <= 0):
        result = state.statisticallyEvaluateForToPlay()
        return store_result(tt, state, result)

    noneFlag = False

    for m in state.get_legal_moves(state.current_player):
        state.play_move(m, state.current_player)
        success = negamax(state, tt, depth - 1)

        if (success != None):
            success = not success
        else:
            noneFlag = True

        state.undo_move()

        if success:
            return store_result(tt, state, True)

    result = None
    if (noneFlag):
        result = store_result(tt, state, None)
    else:
        result = store_result(tt, state, False)

    return result


def negamax_with_moves(state, tt, depth):
    all_moves = set()
    for move in state.get_legal_moves(state.current_player):

        state.play_move(move, state.current_player)

        result = negamax(state, tt, depth - 1)

        state.undo_move()

        if (result == False):
            all_moves.add((True, move))
            break
        elif (result == True):
            all_moves.add(False)
        elif (result == None):
            all_moves.add(None)

    result = eval_all_moves(all_moves)

    return result


def timed_negamax(state, tt, depth, timelimit):
    signal.signal(signal.SIGALRM, immediately_evaluate)
    signal.alarm(timelimit)
    result = None

    result = negamax(state, tt, depth)

    signal.alarm(0)
    return result

def timed_negamax_with_moves(state, tt, depth, timelimit):
    signal.signal(signal.SIGALRM, immediately_evaluate)
    signal.alarm(timelimit)

    result = negamax_with_moves(state, tt, depth)

    signal.alarm(0)

    return result

def eval_all_moves(all_moves):
    all_moves = all_moves - {False}

    if len(all_moves) == 0:
        return False

    all_moves = all_moves - {None}

    if len(all_moves) == 0:
        return None

    for m in all_moves:
        if type(m) == type(tuple()):
            return m

    return None


if __name__ == "__main__":
    board_size = 4
    depth = 10
    timelimit = 3
    state = NoGoBoard(board_size)
    tt = TranspositionTable(state.size)

    print("Player that goes first: {}".format(state.current_player))

    while len(state.get_legal_moves(state.current_player)) != 0:
        i = randint(0, len(state.get_legal_moves(state.current_player)) - 1)
        Rmove = state.get_legal_moves(state.current_player)[i]

        result = None
        try:
            result = timed_negamax_with_moves(state.copy(), tt, depth, timelimit)
        except TimeoutException:
            result = None

        if (type(result) == type(tuple())):
            Rmove = result[1]

        print("FOR PLAYER {}".format(state.current_player))

        state.play_move(Rmove, state.current_player)

        print(result)
        print(Rmove)
        state.display()
        input()

def alphabetaNegamax(state,tt,timelimit,alpha,beta):
    result = tt.lookup(state.code(tt))
    if result != None:
        return result
    if state.is_game_ended():
        result = state.statisticallyEvaluateForToPlay()
        if result:
            result = 1
        else:
            result = -1
        return store_result(tt, state, result)

    # next_state = state.copy()
    for m in state.get_legal_moves(state.current_player):
        # next_state.play_move(m, state.current_player)
        # switch_toPlay(next_state)
        # success = not negamax(next_state, tt)
        # next_state = state.copy()

        state.play_move(m, state.current_player)
        value = -alphabetaNegamax(state,tt,timelimit,-beta,-alpha)
        if value > alpha:
            alpha = value

        state.undo_move()

        if value >= beta:
            return store_result(tt,state, beta)

    return store_result(tt,state,alpha)

def timed_alphabeta_negamax(state, tt, timelimit):
    signal.signal(signal.SIGALRM, immediately_evaluate)
    signal.alarm(timelimit)
    result = None

    result = alphabetaNegamax_with_moves(state, tt,timelimit,-float("inf"),float("inf"))

    signal.alarm(0)
    return result

def alphabetaNegamax_with_moves(state, tt, timelimit,alpha,beta):
    all_moves = set()
    for move in state.get_legal_moves(state.current_player):

        state.play_move(move, state.current_player)

        result = alphabetaNegamax(state, tt,timelimit,alpha, beta)

        state.undo_move()

        if (result == -1):
            all_moves.add((True, move))
            break
        elif (result == 1):
            all_moves.add(False)
        elif (result == None):
            all_moves.add(None)

    result = eval_all_moves(all_moves)

    return result
