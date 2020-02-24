from nogo_board import NoGoBoard
from board_util import GoBoardUtil, \
                        BLACK, WHITE, EMPTY, \
                        BORDER, PASS, MAXSIZE
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


def get_priority(state):
    history = state.moves

    output = set()

    last_points = list()

    if (len(history) >= 2):
        last_points.append(history[-2][0])
        last_points.append(history[-1][0])
    elif (len(history) >= 1):
        last_points.append(history[-1][0])

    for p in last_points:
        output = output | set(state.neighbors[p])

    return output


def negamax(state, tt, depth, move_list=None):
    result = tt.lookup(state.code(tt))
    if result != None:
        return result
    if (state.is_game_ended() or depth <= 0):
        result = state.statisticallyEvaluateForToPlay()
        return store_result(tt, state, result)

    noneFlag = False

    legal_moves = set(filter(state.is_legal_quick, move_list)) 
    priority_moves = get_priority(state) & legal_moves

    for m in priority_moves:
        state.play_blind(m, state.current_player)

        success = negamax(state, tt, depth - 1, move_list - {m})

        if (success != None):
            success = not success
        else:
            noneFlag = True

        state.undo_move()

        if success:
            return store_result(tt, state, True)

    legal_moves = legal_moves - priority_moves

    for m in legal_moves:
        state.play_blind(m, state.current_player)
        
        success = negamax(state, tt, depth - 1, move_list - {m})

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


def negamax_with_moves(state, tt, depth, move_list=None):
    all_moves = set()

    # print(state.moves)
    # print(get_priority(state))

    legal_moves = set(filter(state.is_legal_quick, move_list)) 
    priority_moves = get_priority(state) & legal_moves
  
    ordered_priority_moves = list(priority_moves)
    ordered_priority_moves.sort() 

    for m in ordered_priority_moves:
        # print(format_point(point_to_coord(m, state.size)))

        state.play_blind(m, state.current_player)

        result = negamax(state, tt, depth - 1, move_list - {m})

        state.undo_move()

        if (result == False):
            all_moves.add((True, m))
            return eval_all_moves(all_moves)
        elif (result == True):
            all_moves.add(False)
        elif (result == None):
            all_moves.add(None)

    legal_moves = legal_moves - priority_moves

    for m in legal_moves:
        state.play_blind(m, state.current_player)

        result = negamax(state, tt, depth - 1, move_list - {m})

        state.undo_move()

        if (result == False):
            all_moves.add((True, m))
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

    result = negamax(state, tt, depth, set(state.get_empty_points()))

    signal.alarm(0)
    return result

def timed_negamax_with_moves(state, tt, depth, timelimit):
    signal.signal(signal.SIGALRM, immediately_evaluate)
    signal.alarm(timelimit)

    result = negamax_with_moves(state, tt, depth, set(state.get_empty_points()))

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

    for m in state.get_legal_moves(state.current_player):

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

def point_to_coord(point, boardsize):
    """
    Transform point given as board array index
    to (row, col) coordinate representation.
    Special case: PASS is not transformed
    """
    if point == PASS:
        return PASS
    else:
        NS = boardsize + 1
        return divmod(point, NS)

def format_point(move):
    """
    Return move coordinates as a string such as 'a1', or 'pass'.
    """
    column_letters = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
    #column_letters = "abcdefghjklmnopqrstuvwxyz"
    if move == PASS:
        return "pass"
    row, col = move
    if not 0 <= row < MAXSIZE or not 0 <= col < MAXSIZE:
        raise ValueError
    return column_letters[col - 1]+ str(row)


