import sys
import numpy as np
from collections import OrderedDict
from enum import Enum

class SearchType(Enum):
    DFS = 1
    BFS = 2
    ASTAR = 3

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
        self.fn = 0
        self.gn = 0
        self.hn = 0

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
    #static data member that keeps track of puzzle number
    puzzleNumber = -1    

    def __init__(self, data):
        self.puzzleNumber += 1
        self.size = int(data[0])
        self.maxDepth = int(data[1])
        self.maxLength = int(data[2])
        self.stateString = data[3]
        index = 0
        self.root = Node(None, None, self.stateString, 1, 0)

        # create empty solution path arrays, they will be filled backwards once the solution path is found
        self.solutionPathLabels = list()
        self.solutionPathStates = list()

        

    def printSolutionPath(type):
        if type == SearchType.DFS:
            outputFileName = str(0) + "_dfs_solution.txt"
        elif type == SearchType.BFS:
            outputFileName = str(0) + "_bfs_solution.txt"
        elif type == SearchType.BFS:
            outputFileName = str(0) + "_astar_solution.txt"

        file = open(outputFileName, 'w')

        if self.solutionPathStates.size > 0:
            for i in range(self.solutionPathStates.size - 1, -1, -1):
                outputString = self.solutionPathLabels[i] + "\t"
                for j in range(self.solutionPathStates[i].size):
                    outputString += self.solutionPathStates[i][j] + " "
                outputString += "\n"
                file.write(outputString)
        else:
            file.write("No solution")

        file.close()

    def printSearchPath(type):
        if type == SearchType.DFS:
            outputFileName = str(0) + "_dfs_search.txt"
        elif type == SearchType.BFS:
            outputFileName = str(0) + "_bfs_search.txt"
        elif type == SearchType.BFS:
            outputFileName = str(0) + "_astar_search.txt"

        file = open(outputFileName, 'w')

        for key, value in self.closedList.items():
            outputString = str(value.fn) + " " + str(value.gn) + " " + str(value.hn) + " " + key + "\n"
            file.write(outputString)

        file.close()

#MAIN
fileName = sys.argv[1]
puzzleData = list()
with open(str(fileName)) as file:
    puzzleData = file.readlines()
 
for data in puzzleData:
    data = data.split()
    p = Puzzle(data)
