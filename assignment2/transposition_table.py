class TranspositionTable():
    def __init__(self):
        self.table = dict()

    def store(self, code, score):
        self.table[code] = score

    def lookup(self, code):
        return self.table.get(code)
