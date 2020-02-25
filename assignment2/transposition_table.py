import numpy as np
import random

class TranspositionTable():
    def __init__(self,size):
        self.size = size
        self.table = dict()
        self.code = np.reshape(np.array(random.sample(range(9223372036854775807),size*size*3)),(size*size,3))

    def store(self, code, score):
        self.table[code] = score

    def lookup(self, code):
        return self.table.get(code)
