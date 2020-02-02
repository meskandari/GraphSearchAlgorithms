import sys
import numpy as np

# unused at the moment
class State:
    def __init__(self, M):
        self.state = M

# unused at the moment
class Node:
    def __init__(self, p, s, d, c):
        self.parent = p
        self.state = s
        self.depth = d
        self.cost = c


    def moveTouch(self,givenRow, givenColumn):
        try:
            upper_bound=self.size-1
            #print("Upper bound index is " + str(upper_bound)) -- DEGUG LINE
            row=int(givenRow)
            col=int(givenColumn)

            #FlIP LOCATION
            self.currentState[row][col]=flip(self.currentState[row][col])

            #FLIP LEFT - col axis
            if((col-1)<0):
                '''do nothing'''
            else:
                self.currentState[row][col-1]=flip(self.currentState[row][col-1])


            #FLIP RIGHT - col axis
            if((col+1)>upper_bound):
                '''do nothing'''
            else:
                self.currentState[row][col+1]=flip(self.currentState[row][col+1])

            #FLIP UP - row axis
            if((row-1)<0):
                '''do nothing'''
            else:
                self.currentState[row-1][col]=flip(self.currentState[row-1][col])

            #FLIP DOWN - row axis
            if((row+1)>upper_bound):
                '''do nothing'''
            else:
                self.currentState[row+1][col]=flip(self.currentState[row+1][col])
        except IndexError:
            print("One or more specified indices are out of bounds for Node.moveTouch(self, givenRow, givenColumn)")

    def printArray(self):
        flat = np.ravel(self.currentState)
        for i in flat:
            print(i,end =" ")
        print()

    def flip(value):
        if (value==0):
            return 1
        else:
            return 0

class Puzzle:
    def __init__(self, data):
        self.size = int(data[0])
        self.maxDepth = int(data[1])
        self.maxLength = int(data[2])
        self.stateString = data[3]

        index = 0
        M = np.empty([self.size, self.size], dtype=int)
        for i in range(len(M)):
            for j in range(len(M[i])):
                M[i,j] = int(self.stateString[index])
                index += 1
        
        self.initialState = M
        self.currentState = M

        # construct mask matrix
        self.mask = np.empty([self.size+2, self.size+2], dtype=int)
        for row in range(len(self.mask)):
            for column in range(len(self.mask[row])):
                # if top row or bottom row, pad with 0s
                if row == 0 or row == (len(self.mask) - 1):
                    self.mask[row, column] = 0
                # if left column or right column, pad with 0s
                elif column == 0 or column == (len(self.mask) - 1):
                    self.mask[row, column] = 0
                # otherwise place 1s in inner square
                else:
                    self.mask[row, column] = 1

    # grab the immediate neighbours of the specified indices
    # verifies the neighbours against the mask so it doesn't try to grab out of bounds
    def getNeighbours(self, row, column):
        try:
            index = (row * self.size) + column
            indices = list()
            # top
            if (self.mask[row, column+1] == 1):
                indices.append(index - self.size)
            # bottom
            if (self.mask[row+2, column+1] == 1):
                indices.append(index + self.size)
            # left
            if (self.mask[row+1, column] == 1):
                indices.append(index - 1)
            # right
            if (self.mask[row+1, column+2] == 1):
                indices.append(index + 1)
        except IndexError:
            print("One or more specified indices are out of bounds for Puzzle.getNeighbours(row, column)")
            return None
        return self.currentState.take(indices)




fileName = sys.argv[1]
puzzleData = list()
with open(str(fileName)) as file:
    puzzleData = file.readlines()

for data in puzzleData:
    data = data.split()
    p = Puzzle(data)
    print(p.getNeighbours(2, 2))