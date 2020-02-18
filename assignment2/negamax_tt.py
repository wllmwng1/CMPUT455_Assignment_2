from board_util import GoBoardUtil, \
                        BLACK, WHITE, EMPTY
import signal


def immediately_evaluate(state, tt):
    raise Exception;


def store_result(tt, state, result):
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

    signal.signal(signal.SIGALRM, immediately_evaluate)

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
    signal.alarm(timelimit)

    result = False
    try:
        result = negamax(state, tt)
    except:
        result = state.statisticallyEvaluateForToPlay()
        print("current_player is: {}".format(state.current_player))
        print("black: {}".format(BLACK))
        print("result is: {}".format(result))
    return result



