from board_util import GoBoardUtil, \
                        BLACK, WHITE, EMPTY

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

