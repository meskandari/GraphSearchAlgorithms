import sys
import numpy as np
from operator import itemgetter, attrgetter
from collections import OrderedDict
from enum import Enum
import time



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

class HeuristicType(Enum):
    MARTIN = 1
    MARYAM = 2
    JASON = 3

# The Node class contains all the attributes and methods needed to manage a node in a search tree
class Node:

    #static dictionary that has the neighbors indexes per digit 
    #<key,Value> == <digit , set Of neighbor's indexes digit included>
    #should update only if the size of new puzzle is different
    flippingIndexesByDigit = {}
    staticSize = -1
    # constructor
    def __init__(self, parentNode, index, size, stateStr, stateBinary, depth, cost, heuristic, label = "0", hn=0):
        
        # assign the dictionary key values
        #we use this to copmare with set of 1's indexes in each node to calculate h(n)
        if Node.staticSize!=size:
             Node.staticSize=size
             Node.flippingIndexesByDigit = PuzzleUtil.createDictOfFlipIndexes(size)
             #print(Node.flippingIndexesByDigit)

        self.parent = parentNode
        self.index = index
        self.stateStr = stateStr
        self.depth = depth
        self.cost = cost
        self.offset = size
        self.stateBinary = np.empty(self.offset * self.offset, dtype=int)
        self.children = list()
        self.label = label
        self.gn = depth
        self.hn = hn
        self.fn = self.hn + self.gn
        self.heuristic = heuristic

           
        if depth == 0:
            for i in range(len(self.stateBinary)):
                self.stateBinary[i] = int(self.stateStr[i])
        else:
            self.stateBinary = stateBinary
        
        if heuristic == HeuristicType.MARTIN:
            self.evaluateNode()
        elif heuristic == HeuristicType.MARYAM:
            self.evaluateNode_m()
        else:
            self.evaluateNode_j()

    # create the connected children of this node
    def generateChildren(self, searchType=0):
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
            n = Node(self, i, self.offset, stateString , arr, self.depth + 1, self.cost + 1, self.heuristic, PuzzleUtil.generateNodeLabel(row, col))
            self.children.append(n)
        
        if (searchType==SearchType.DFS):
            # sort the children in reverse order
            self.children = sorted(self.children , key = attrgetter('stateStr'), reverse = True)
    
    def flipXOR(self, digit):
        # create a zero'd array of the same size as the current node's state
        binaryPattern = np.zeros(len(self.stateBinary), dtype = 'int')
        
        # get the indices of the immediate neighbours of this cell, change the appropriate indices to 1
        indicesToChange = self.getNeighbours(digit)
        #test = self.stateBinary[:]
        for i in indicesToChange:
            #test[i]=1-test[i]
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

    #BFS Heuristics
    def evaluateNode(self):  
        #print(self.stateBinary)
        distanceToGoal = np.count_nonzero(self.stateBinary == 1)
        if distanceToGoal<6:
            self.hn = min((distanceToGoal%3),(distanceToGoal%4),(distanceToGoal%5))
        else:
            self.hn = distanceToGoal
    
    #BFS Heuristics_maryam 
    def evaluateNode_m(self):  
        indexesOfOnes = set()
        for i in range(len(self.stateBinary)):
            if self.stateBinary[i]==1:
                indexesOfOnes.add(i)
        #print(indexesOfOnes)
        differenceSet=set()
        for i in range(len(self.flippingIndexesByDigit)):
            set1 = self.flippingIndexesByDigit.get(i)
            if set1.issubset(indexesOfOnes):
             indexesOfOnes-=set1
            if len(indexesOfOnes)<3:
                break
        #compute distance between remaining indexes of ones 
        #try to evaluate if the ones near each other or not
        if(len(indexesOfOnes)!=0)&(len(indexesOfOnes)< 4 ):
            sortedList = sorted(indexesOfOnes)
            self.hn=sortedList[len(sortedList)-1]-sortedList[0]
        self.hn+= len(indexesOfOnes)
        self.fn = self.hn + self.gn
        indexesOfOnes.clear()
       #print(differenceSet)

    #BFS Heuristics_jason
    def evaluateNode_j(self):
        if(self.parent):
            neighbors = self.getNeighbours(self.index)
            cost = 1 # base cost for moving down 1 depth
            for i in range(len(neighbors)):
                if self.stateBinary[i] == 1:
                    cost += 1
            self.gn = self.parent.gn + cost

            binCountParent = np.bincount(self.parent.stateBinary)
            binCountSelf = np.bincount(self.stateBinary)
            if(binCountSelf[0] == len(self.stateBinary)):
                self.hn = 0
            else:
                self.hn = abs((float)(binCountParent[1] - binCountSelf[1])) / len(neighbors) + binCountSelf[1]
            self.fn = self.gn + self.hn

            
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
    
    #return the idexes of given digit as a set
    @staticmethod
    def getNeighboursIndexOfGivenDigit(size, digit):
        validIndices = set()
        lastDigitIndex = size*size
        

        # populate the valid Indices list with this cell's index and it's immediate neighbours' indices
        if -1 < digit < (lastDigitIndex+1):
            validIndices.add(digit)

            # top neighbours
            if (digit - size) >= 0:
                validIndices.add(digit - size)

            # left neighbours
            if (digit % size) != 0:
                validIndices.add(digit-1)

            # bottom neighbour
            if (digit + size) < (lastDigitIndex+1):
                validIndices.add(digit + size)

            # right neighbours
            if ((digit + 1) % size) != 0:
                validIndices.add(digit+1)

        return validIndices

    @staticmethod
    def createDictOfFlipIndexes(size):
        flippingIndexes = set()
        flippingIndexesByDigit = {}

        for i in range (size * size):
            flippingIndexes= PuzzleUtil.getNeighboursIndexOfGivenDigit(size , i)
            flippingIndexesByDigit[i] = flippingIndexes
        return flippingIndexesByDigit

# The puzzle class represents a particular puzzle configuration
# the root node is the puzzle's initial state
# the class contains methods to solve the puzzle using Depth First Search, generate solution and search paths,
# and finally to print the results to a file
class Puzzle:
    # static data member that keeps track of puzzle number
    puzzleNumber = -1


    def __init__(self, data, heuristic):
        Puzzle.puzzleNumber += 1
        if Puzzle.puzzleNumber > 3:
            Puzzle.puzzleNumber = 0
        self.size = int(data[0])
        self.maxDepth = int(data[1])
        self.maxLength = int(data[2])
        self.stateString = data[3]
        self.root = Node(None, 0, self.size, self.stateString, None, 0, 0, heuristic)
        self.searchPathLength = 0
        self.heuristic = heuristic

        # initialize closed list and open list
        self.closedList = OrderedDict()
        self.openList = OrderedDict()

        # create empty solution path arrays, they will be filled backwards once the solution path is found
        self.solutionPath = list()

       
    
    # recursively solve the puzzle using depth first search
    def puzzleDFS(self, node):
        startTime = time.time()
        while(node):
            if node.depth >= self.maxDepth:
                # pop next element in stack
                node=self.openList.popitem(last = True)
                
                # if stack is empty, print "No Solution"
                if self.openList is None:
                    endTime = time.time() 
                    self.printSolutionPath(SearchType.DFS)
                    self.printSearchPath(SearchType.DFS)
                    print("Puzzle #" + str(self.puzzleNumber) + " no solution!")
                    node= None
                    print("This conclusion was reached in %g seconds via DFS" % (endTime - startTime))
                    self.clearPuzzle()
                    break
        
            # test if the current node is the goal state
            elif PuzzleUtil.GoalStateTest(node):
                endTime = time.time() 
                self.closedList[node.stateStr] = node
                self.createSolutionPath(node)
                self.printSolutionPath(SearchType.DFS)
                self.printSearchPath(SearchType.DFS)
                print("Puzzle #" + str(self.puzzleNumber) + " solution found!")
                node= None
                print("This conclusion was reached in %g seconds via DFS" % (endTime - startTime))
                self.clearPuzzle()
                break

            # the current node wasn't the goal state, so add it to the closed list,
            # generate it's children and recursively search the open list
            else:
                # add node.state to the closed list
                self.closedList[node.stateStr] = node

                # generate the node's children
                node.generateChildren(SearchType.DFS)

                # verify that children depth is less than max before adding to open list
                for item in node.children:
                    if (item.depth < self.maxDepth) and (item.stateStr not in self.closedList) and (item.stateStr not in self.openList):
                        self.openList[item.stateStr] = item
            

                # if stack is empty, print "No Solution"
                if not bool(self.openList):
                    endTime = time.time() 
                    self.printSolutionPath(SearchType.DFS)
                    self.printSearchPath(SearchType.DFS)
                    print("Puzzle #" + str(self.puzzleNumber) + " no solution!")
                    node= None
                    print("This conclusion was reached in %g seconds via DFS" % (endTime - startTime))
                    self.clearPuzzle()
                    break
                else:
                    # pop next element on the Stack and visit
                    node=self.openList.popitem(last = True)[1]

    def puzzleBFS(self, node):
        startTime = time.time()
        while(node):
            #increase cost of search
            self.searchPathLength+=1

            # verify is maximum search path length is not reached, if so exit
            if self.searchPathLength >= self.maxLength:
                endTime = time.time() 
                self.printSolutionPath(SearchType.BFS)
                self.printSearchPath(SearchType.BFS)
                self.printToReport(SearchType.BFS, "timeout", endTime - startTime)
                #print("Puzzle #" + str(self.puzzleNumber) + " no solution! Timed-Out - BFS - %g seconds" % (endTime - startTime))
                node= None
                #print("This conclusion was reached in %g seconds using BFS" % (endTime - startTime))
                #print("Timed-out after reaching max search path of %s " % self.searchPathLength)
                self.clearPuzzle()
                break
 
        
            # test if the current node is the goal state
            elif PuzzleUtil.GoalStateTest(node):
                endTime = time.time() 
                self.closedList[node.stateStr] = node
                self.createSolutionPath(node)
                self.printSolutionPath(SearchType.BFS)
                self.printSearchPath(SearchType.BFS)
                self.printToReport(SearchType.BFS, "solved", endTime - startTime)
                #print("Puzzle #" + str(self.puzzleNumber) + " solution found! BFS - %g seconds" % (endTime - startTime))
                node= None
                #print("This conclusion was reached in %g seconds using BFS" % (endTime - startTime))
                self.clearPuzzle()
                break

            # the current node wasn't the goal state, so add it to the closed list,
            # generate it's children and recursively search the open list
            else:
                # add node.state to the closed list
                self.closedList[node.stateStr] = node

                # generate the node's children
                node.generateChildren()

                # verify that children depth is less than max before adding to open list
                for item in node.children:
                    if (item.stateStr not in self.closedList) and (item.stateStr not in self.openList):
                        self.openList[item.stateStr] = item
            
                # sort the open list in ascending order of h(n)
                self.sortOpenList(SearchType.BFS)
                # if list is empty, print "No Solution"
                if not bool(self.openList):
                    endTime = time.time()                    
                    self.printSolutionPath(SearchType.BFS)
                    self.printSearchPath(SearchType.BFS)
                    self.printToReport(SearchType.BFS, "timeout", endTime - startTime)
                    #print("Puzzle #" + str(self.puzzleNumber) + " no solution! BFS - %g seconds" % (endTime - startTime))
                    node= None
                    #print("This conclusion was reached in %g seconds using BFS" % (endTime - startTime))
                    self.clearPuzzle()
                    break
                else:
                    # pop next element on the list and visit
                    node=self.openList.popitem(last = False)[1]
    
    def puzzleASTAR(self, node):
        startTime = time.time()
        while(node):
            #increase cost of search
            self.searchPathLength+=1

            # verify is maximum search path length is not reached, if so exit
            if self.searchPathLength >= self.maxLength:
                endTime = time.time()
                self.printSolutionPath(SearchType.ASTAR)
                self.printSearchPath(SearchType.ASTAR)
                self.printToReport(SearchType.ASTAR, "timeout", endTime - startTime)
                #print("Puzzle #" + str(self.puzzleNumber) + " no solution! Timed-out - A* - %g seconds" % (endTime - startTime))
                node= None
                #print("This conclusion was reached in %g seconds using A*" % (endTime - startTime))
                #print("Timed-out after reaching max search path of %s " % self.searchPathLength)
                self.clearPuzzle()
                break
 
        
            # test if the current node is the goal state
            elif PuzzleUtil.GoalStateTest(node):
                endTime = time.time()
                self.closedList[node.stateStr] = node
                self.createSolutionPath(node)
                self.printSolutionPath(SearchType.ASTAR)
                self.printSearchPath(SearchType.ASTAR)
                self.printToReport(SearchType.ASTAR, "solved", endTime - startTime)
                #print("Puzzle #" + str(self.puzzleNumber) + " solution found! A* - %g seconds" % (endTime - startTime))
                node= None
                #print("This conclusion was reached in %g seconds using A*" % (endTime - startTime))
                self.clearPuzzle()
                break

            # the current node wasn't the goal state, so add it to the closed list,
            # generate it's children and recursively search the open list
            else:
                # add node.state to the closed list
                self.closedList[node.stateStr] = node

                # generate the node's children
                node.generateChildren()

                # verify that children depth is less than max before adding to open list
                for item in node.children:
                    #TODO -- ADD 'AND' CODE TO UPDATE ENTRY OF STATE FOUND WITH BETTER F(N) IN OPEN LIST
                    # no need to add additional condition since the line 428 does the same job
                    if (item.stateStr not in self.closedList) :
                        if(item.stateStr in self.openList):
                            if(item.fn < self.openList[item.stateStr].fn):
                                self.openList[item.stateStr] = item # this line updates the value if the key exists otherwise it add as new <key,value>
                        else:
                            self.openList[item.stateStr] = item
                    #else:
                    #    if item.fn < self.closedList[item.stateStr].fn:
                    #        self.closedList[item.stateStr] = item

                # sort the open list in ascending order of h(n)
                self.sortOpenList(SearchType.ASTAR)
                # if list is empty, print "No Solution"
                if not bool(self.openList):
                    endTime = time.time()
                    self.printSolutionPath(SearchType.ASTAR)
                    self.printSearchPath(SearchType.ASTAR)
                    self.printToReport(SearchType.ASTAR, "timeout", endTime - startTime)
                    #print("Puzzle #" + str(self.puzzleNumber) + " no solution! A* - %g seconds" % (endTime - startTime))
                    node= None
                    #print("This conclusion was reached in %g seconds using A*" % (endTime - startTime))
                    self.clearPuzzle()
                    break
                else:
                    # pop next element on the list and visit
                    node=self.openList.popitem(last = False)[1]

    def sortOpenList(self,type):
       if type == SearchType.BFS:
            self.openList = OrderedDict(sorted(self.openList.items(), key = lambda node: node[1].hn))
       elif type == SearchType.ASTAR:
            self.openList =OrderedDict(sorted(self.openList.items(), key = lambda node: node[1].fn))

    def clearPuzzle(self):
        self.root = Node(None, 0, self.size, self.stateString, None, 0, 0, self.heuristic)
        self.searchPathLength=0
        self.closedList.clear()
        self.openList.clear()
        del self.solutionPath[:]

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
        elif type == SearchType.ASTAR:
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
        elif type == SearchType.ASTAR:
            outputFileName = str(self.puzzleNumber) + "_astar_search.txt"

        file = open(outputFileName, 'w')

        if type == SearchType.DFS:
            for key, value in self.closedList.items():
                outputString = str(0) + " " + str(0) + " " + str(0) + " " + str(key) + "\n"
                file.write(outputString)
        elif type == SearchType.BFS:
            for key, value in self.closedList.items():
                outputString = str(0) + " " + str(0) + " " + str(value.hn) + " " + str(key) + "\n"
                file.write(outputString)
        elif type == SearchType.ASTAR:
            for key, value in self.closedList.items():
                outputString = str(value.fn) + " " + str(value.gn) + " " + str(value.hn) + " " + str(key) + "\n"
                file.write(outputString)

        file.close()

    def printToReport(self, type, status, time):
        if type == SearchType.DFS:
            outputFileName = str(self.puzzleNumber) + "_dfs_performance.txt"
        elif type == SearchType.BFS:
            outputFileName = str(self.puzzleNumber) + "_bfs_performance.txt"
        elif type == SearchType.ASTAR:
            outputFileName = str(self.puzzleNumber) + "_astar_performance.txt"

        htype = ""
        if self.heuristic == HeuristicType.MARTIN:
            hType = "martin"
        elif self.heuristic == HeuristicType.MARYAM:
            hType = "maryam"
        else:
            hType = "jason"

        file = open(outputFileName, 'a')
        file.write(str(self.puzzleNumber) + ", " + hType + ", "+ status + ", " + str(time) + "\n")
        file.close()
        

# MAIN

# read the filename from the first command line argument
#fileName = sys.argv[1]
fileName = "test.txt"
puzzleData = list()

# read the puzzle data into a list
with open(str(fileName)) as file:
    puzzleData = file.readlines()

# split the data by whitespace, and create a Puzzle object for each one,
# then use depth first search to solve each puzzle
heuristic = HeuristicType.MARTIN
for i in range(0, 3):
    for j in range(10):
        for data in puzzleData:
            data = data.split()
            p = Puzzle(data, heuristic)
            #print(data)
            #p.puzzleDFS(p.root)
            p.puzzleBFS(p.root)
            p.puzzleASTAR(p.root)
    if heuristic == HeuristicType.MARTIN:
        heuristic = HeuristicType.MARYAM
    else:
        heuristic = HeuristicType.JASON

