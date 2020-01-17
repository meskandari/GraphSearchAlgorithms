import sys
import numpy as np

class State:
    def __init__(self, M):
        self.state = M

class Node:
    def __init__(self, p, s, d, c):
        self.parent = p
        self.state = s
        self.depth = d
        self.cost = c

fileName = sys.argv[1]
puzzleData = list()
with open(str(fileName)) as file:
    puzzleList = f.readlines().split()

def initialize(p):
    size = p[0]
    maxDepth = p[1]
    maxLength = p[2]
    initialState = p[3]

    index = 0
    global M
    M = np.empty([size, size], dtype=int)
    for i in M:
        for j in M[i]:
            M[i,j] = initialState[index]
            index += 1

for p in puzzleList:
    initialize(p)
    solve(p)