from board_util import GoBoardUtil, \
                        BLACK, WHITE, EMPTY
import time
import signal


def immediately_evaluate(signum, frame):
    raise Exception("TIMELIMIT ERROR: timed out");


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


def negamax(state, tt):
    result = tt.lookup(state.code(tt))
    if result != None:
        return result
    if state.is_game_ended():
        result = state.statisticallyEvaluateForToPlay()
        return store_result(tt, state, result)

    # next_state = state.copy()
    for m in state.get_legal_moves(state.current_player):
        # next_state.play_move(m, state.current_player)
        # switch_toPlay(next_state)
        # success = not negamax(next_state, tt)
        # next_state = state.copy()

        state.play_move(m, state.current_player)
        success = not negamax(state, tt)
        state.undo_move()

        if success:
            return store_result(tt, state, True)

    return store_result(tt, state, False)


def timed_negamax(state, tt, timelimit):

    print("timelimit is: {}".format(timelimit))

    signal.signal(signal.SIGALRM, immediately_evaluate)

    signal.alarm(timelimit)

    result = None

    # result = negamax(state, tt)

    try:
        # signal.alarm(timelimit)
        result = negamax(state, tt)
    except Exception as e:
        print("Exception raised: {}".format(e))
        signal.alarm(0)
        return result

    signal.alarm(0)
    return result
