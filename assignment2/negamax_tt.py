from board_util import GoBoardUtil

def negamax(state, tt):
    print("negamax now exists!")

    i = 0

    while (not state.is_game_ended()):
        current_player = state.current_player
        move = GoBoardUtil.generate_random_move(state, current_player, False)
        state.play_move(move, current_player)
        print("move {}: {}".format(i, move))
        print(state.display())
        print()
        i += 1

    print("finished")

    return None

