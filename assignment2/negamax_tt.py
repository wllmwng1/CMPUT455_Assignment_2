from board_util import GoBoardUtil, \
                        BLACK, WHITE, EMPTY
import time
import signal


def immediately_evaluate(signum, frame):
    raise Exception();


def store_result(tt, state, result):
    tt.store(state.code(), result)
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
    if state.is_game_ended():
        result = state.statisticallyEvaluateForToPlay()
        return store_result(tt, state, result)

    next_state = state.copy()
    for m in state.get_legal_moves(state.current_player):
        next_state.play_move(m, state.current_player) 
        switch_toPlay(next_state)

        success = not negamax(next_state, tt)

        next_state = state.copy()

        if success:
            return store_result(tt, state, True)

    return store_result(tt, state, True)


def timed_negamax(state, tt, timelimit):

    print("timelimit is: {}".format(timelimit))


    signal.signal(signal.SIGALRM, immediately_evaluate)

    signal.alarm(1000)

    result = None
    try:
        # signal.alarm(timelimit)
        result = negamax(state, tt)
    except:
        print("Exception raised")

    signal.alarm(0)

    return result



