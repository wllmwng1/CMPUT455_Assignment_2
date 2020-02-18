# Cmput 455 sample code
# Boolean Negamax
# Written by Martin Mueller

def storeResult(tt, state, result):
    tt.store(state.code(), result)
    return result

def negamaxBoolean(state, tt):
    result = tt.lookup(state.code())
    if result != None:
        return result
    if state.endOfGame():
        result = state.staticallyEvaluateForToPlay()
        return storeResult(tt, state, result)
    for m in state.legalMoves():
        state.play(m)
        success = not negamaxBoolean(state, tt)
        state.undoMove()
        if success:
            return storeResult(tt, state, True)
    return storeResult(tt, state, False)
