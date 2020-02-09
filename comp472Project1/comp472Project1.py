import sys
import numpy as np
from operator import itemgetter, attrgetter
from collections import OrderedDict
from enum import Enum

# An enum class for labelling cells in the puzzle matrix
class RowLabel(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7
    I = 8
    J = 9

# An enum class for flagging the type of search algorithm to use
class SearchType(Enum):
    DFS = 1
    BFS = 2
    ASTAR = 3

# The Node class contains all the attributes and methods needed to manage a node in a search tree
class Node:

    # constructor
    def __init__(self, parentNode, index, size, stateStr, stateBinary, depth, cost, label = "0"):
        self.parent = parentNode
        self.index = index
        self.stateStr = stateStr
        self.depth = depth
        self.cost = cost
        self.offset = size
        self.stateBinary = np.empty(self.offset * self.offset, dtype=int)
        self.children = list()
        self.label = label
        self.fn = 0
        self.gn = 0
        self.hn = 0
           
        if depth == 0:
            for i in range(len(self.stateBinary)):
                self.stateBinary[i] = int(self.stateStr[i])
        else:
            self.stateBinary = stateBinary

    # create the connected children of this node
    def generateChildren(self):
        # grab the coordinates for each cell
        # perform a bitwise XOR on the cell and it's immediate neighbours
        for i in range(len(self.stateBinary)):
            row = i // self.offset
            col = i % self.offset
            arr = self.flipXOR(i)

            # remove whitespace and brackets
            stateString = np.array2string(arr).replace(" ", "")
            stateString = str(stateString)[1:-1]

            # generate a new node using the flipped state and add it to this node's list of children
            n = Node(self, i, self.offset, stateString , arr, self.depth + 1, self.cost + 1, PuzzleUtil.generateNodeLabel(row, col))
            self.children.append(n)

        # sort the children in reverse order
        self.children = sorted(self.children , key = attrgetter('stateStr'), reverse = True)
    
    def flipXOR(self, digit):
        # create a zero'd array of the same size as the current node's state
        binaryPattern = np.zeros(len(self.stateBinary), dtype = 'int')
        
        # get the indices of the immediate neighbours of this cell, change the appropriate indices to 1
        indicesToChange = self.getNeighbours(digit)
        for i in indicesToChange:
            binaryPattern[i] = 1
       
        return np.bitwise_xor(binaryPattern, self.stateBinary)

    def getNeighbours(self, digit):
        validIndices = list()

        # populate the valid Indices list with this cell's index and it's immediate neighbours' indices
        if -1 < digit < len(self.stateBinary):
            validIndices.append(digit)

            # top neighbours
            if (digit - self.offset) >= 0:
                validIndices.append(digit - self.offset)

            # left neighbours
            if (digit % self.offset) != 0:
                validIndices.append(digit-1)

            # bottom neighbour
            if (digit + self.offset) < len(self.stateBinary):
                validIndices.append(digit + self.offset)

            # right neighbours
            if ((digit + 1) % self.offset) != 0:
                validIndices.append(digit+1)

        return validIndices
            
# A class containing useful utility methods
class PuzzleUtil:

    def __init__(self):
        pass

    # method to generate node labels
    @staticmethod
    def generateNodeLabel(row, col):
        label = "".join([RowLabel(row).name, str(col + 1)])
        return label

    # method that compares the given node's state to a zero array, returning true if they are equal
    @staticmethod
    def GoalStateTest(node):
        zeroArr = np.zeros(len(node.stateBinary), dtype = 'int')
        return np.array_equal(zeroArr, node.stateBinary)

    # print the values in the array (for debugging)
    @staticmethod
    def printArray(arr):
        flat = np.ravel(arr)
        for i in flat:
            print(i, end = " ")
        print()

    # converts a binary string to it's decimal value
    @staticmethod
    def stringToDecimal(stateStr):
        return int(stateStr, 2)

# The puzzle class represents a particular puzzle configuration
# the root node is the puzzle's initial state
# the class contains methods to solve the puzzle using Depth First Search, generate solution and search paths,
# and finally to print the results to a file
class Puzzle:
    # static data member that keeps track of puzzle number
    puzzleNumber = -1

    def __init__(self, data):
        Puzzle.puzzleNumber += 1
        self.size = int(data[0])
        self.maxDepth = int(data[1])
        self.maxLength = int(data[2])
        self.stateString = data[3]
        self.root = Node(None, 0, self.size, self.stateString, None, 0, 0)

        # initialize closed list and open list
        self.closedList = OrderedDict()
        self.openList = OrderedDict()

        # create empty solution path arrays, they will be filled backwards once the solution path is found
        self.solutionPath = list()
    
    # recursively solve the puzzle using depth first search
    def puzzleDFS(self, node):
        if node.depth >= self.maxDepth:
            # pop next element in stack
            self.puzzleDFS(self.openList.popitem(last = True))
                
            # if stack is empty, print "No Solution"
            if self.openList is None:
                self.printSolutionPath(SearchType.DFS)
                self.printSearchPath(SearchType.DFS)
                print("Puzzle #" + str(self.puzzleNumber) + " no solution!")
        
        # test if the current node is the goal state
        elif PuzzleUtil.GoalStateTest(node):
            self.closedList[node.stateStr] = node
            self.createSolutionPath(node)
            self.printSolutionPath(SearchType.DFS)
            self.printSearchPath(SearchType.DFS)
            print("Puzzle #" + str(self.puzzleNumber) + " solution found!")

        # the current node wasn't the goal state, so add it to the closed list,
        # generate it's children and recursively search the open list
        else:
            # add node.state to the closed list
            self.closedList[node.stateStr] = node

            # generate the node's children
            node.generateChildren()

            # verify that children depth is less than max before adding to open list
            for item in node.children:
                if (item.depth < self.maxDepth) and (item.stateStr not in self.closedList) and (item.stateStr not in self.openList):
                    self.openList[item.stateStr] = item
            

            # if stack is empty, print "No Solution"
            if not bool(self.openList):
                self.printSolutionPath(SearchType.DFS)
                self.printSearchPath(SearchType.DFS)
                print("Puzzle #" + str(self.puzzleNumber) + " no solution!")
            else:
                # pop next element on the Stack and visit
                self.puzzleDFS(self.openList.popitem(last = True)[1])

    # create a solution path from the goal state back to the root node
    def createSolutionPath(self, node):
        n = node
        if n.parent is not None:
            while(True):
                self.solutionPath.append(n)
                n = n.parent
                if n.parent is None:
                    self.solutionPath.append(n)
                    break

    # output the solution path to a file named after the given search algorithm
    def printSolutionPath(self, type):
        if type == SearchType.DFS:
            outputFileName = str(self.puzzleNumber) + "_dfs_solution.txt"
        elif type == SearchType.BFS:
            outputFileName = str(self.puzzleNumber) + "_bfs_solution.txt"
        elif type == SearchType.BFS:
            outputFileName = str(self.puzzleNumber) + "_astar_solution.txt"

        file = open(outputFileName, 'w')

        # if the solution path contains some items, then output them to a file
        if len(self.solutionPath) > 0:
            for i in range(len(self.solutionPath) - 1, -1, -1):
                outputString = self.solutionPath[i].label + "\t"
                for j in range(len(self.solutionPath[i].stateStr)):
                    outputString += self.solutionPath[i].stateStr[j] + " "
                outputString += "\n"
                file.write(outputString)
        # otherwise there is no solution
        else:
            file.write("No solution")

        file.close()

    # output the search path to a file named after the given search algorithm
    def printSearchPath(self, type):
        if type == SearchType.DFS:
            outputFileName = str(self.puzzleNumber) + "_dfs_search.txt"
        elif type == SearchType.BFS:
            outputFileName = str(self.puzzleNumber) + "_bfs_search.txt"
        elif type == SearchType.BFS:
            outputFileName = str(self.puzzleNumber) + "_astar_search.txt"

        file = open(outputFileName, 'w')

        for key, value in self.closedList.items():
            outputString = str(value.fn) + " " + str(value.gn) + " " + str(value.hn) + " " + str(key) + "\n"
            file.write(outputString)

        file.close()

    

# MAIN

# read the filename from the first command line argument
fileName = sys.argv[1]
puzzleData = list()

# read the puzzle data into a list
with open(str(fileName)) as file:
    puzzleData = file.readlines()

# split the data by whitespace, and create a Puzzle object for each one,
# then use depth first search to solve each puzzle
for data in puzzleData:
    data = data.split()
    p = Puzzle(data)
    p.puzzleDFS(p.root)
