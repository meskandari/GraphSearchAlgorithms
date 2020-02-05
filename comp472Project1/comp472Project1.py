import sys
import numpy as np

# unused at the moment
class State:
    def __init__(self, state):
        self.state = state

class Node:
    def __init__(self, parent, index, state, depth, cost):
        self.parent = parent
        self.index = index
        self.state = state
        self.depth = depth
        self.cost = cost
        self.children = list()

    def generateChildren(self, max):
        for i in range(max):
            if(i != self.index):
                s = np.array(self.state)
                coords = np.unravel_index(i, s.shape)
                s = Puzzle_Util.moveTouch(s, s.shape[0], coords[0], coords[1])
                # cost + 1 for now
                n = Node(self, i, s, self.depth + 1, self.cost + 1)
                self.children.append(n)

class Puzzle_Util:

    def __init__(self):
        pass

     # instance method to generate node labels
    @staticmethod
    def generateNodeLabel(row , col):
        label_str = "".join([Row_Label(row).name, str(col+1)])
        return(label_str)

    def printArray(arr):
        flat = np.ravel(arr)
        for i in flat:
            print(i,end =" ")
        print()

    @staticmethod
    def flip(value):
        return 1 if value == 0 else 0

    @staticmethod
    def moveTouch(state, size, givenRow, givenColumn):
        try:
            upper_bound=size-1
            #print("Upper bound index is " + str(upper_bound)) -- DEGUG LINE
            row=int(givenRow)
            col=int(givenColumn)

            #FlIP LOCATION
            state[row][col]=Puzzle_Util.flip(state[row][col])

            #FLIP LEFT - col axis
            if((col-1)<0):
                '''do nothing'''
            else:
                state[row][col-1]=Puzzle_Util.flip(state[row][col-1])


            #FLIP RIGHT - col axis
            if((col+1)>upper_bound):
                '''do nothing'''
            else:
                state[row][col+1]=Puzzle_Util.flip(state[row][col+1])

            #FLIP UP - row axis
            if((row-1)<0):
                '''do nothing'''
            else:
                state[row-1][col]=Puzzle_Util.flip(state[row-1][col])

            #FLIP DOWN - row axis
            if((row+1)>upper_bound):
                '''do nothing'''
            else:
                state[row+1][col]=Puzzle_Util.flip(state[row+1][col])

            return state
        except IndexError:
            print("One or more specified indices are out of bounds for Node.moveTouch(self, givenRow, givenColumn)")

    def evaluateState(arr,position):
        #extract row and col index
        location = position.split(",")
        row=int(location[0])
        col=int(location[1])
        #initialize search result coordinates
        i,j=0,0
        #run search for value
        searchRows,searchCols=np.where(arr == 0)
        #iterate through result to spit out first result
        for index,value in enumerate(searchRows):
            if(searchRows[index]>row):
                #print(searchRows[index])
                i=searchRows[index]
                j=searchCols[index]
                #print("X: " + str(searchRows[index]) + " Y: " + str(searchCols[index]))
                break
            if(searchRows[index]==row):
                #print(searchRows[index])            
                if(searchCols[index]>col):
                    i=searchRows[index]
                    j=searchCols[index]
                    #print("X: " + str(searchRows[index]) + " Y: " + str(searchCols[index]))
                    break
                else:
                    continue
        output=list()
        output.append(i)
        output.append(j)
        return output

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
        self.root = Node(None, None, self.initialState, 1, 0)

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

    print("parent node is: ", p.root)
    p.root.generateChildren(p.size * p.size)
    for i in range(len(p.root.children)):
        print("child ", p.root.children[i], " of parent ", p.root.children[i].parent)

    print("state of child 0: ")
    print(p.root.children[0].state)
    print("parent's state is: ")
    print(p.root.children[0].parent.state)