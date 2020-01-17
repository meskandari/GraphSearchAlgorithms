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

def initialize(p):
    size = int(p[0])
    maxDepth = int(p[1])
    maxLength = int(p[2])
    initialState = p[3]

    index = 0
    M = np.empty([size, size], dtype=int)
    for i in range(len(M)):
        for j in range(len(M[i])):
            M[i,j] = int(initialState[index])
            index += 1

fileName = sys.argv[1]
puzzleData = list()
with open(str(fileName)) as file:
    puzzleData = file.readlines()

for p in puzzleData:
    p = p.split()
    initialize(p)
    #solve(p)