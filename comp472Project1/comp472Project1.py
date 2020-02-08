import sys
import numpy as np
from operator import itemgetter, attrgetter
from collections import OrderedDict
from enum import Enum

class Row_Label(Enum):
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

class SearchType(Enum):
    DFS = 1
    BFS = 2
    ASTAR = 3

# unused at the moment
class State:
    def __init__(self, state):
        self.state = state

class Node_BinaryRep:

    def __init__(self, parent_Node,index, size, stateStr,state_as_BinaryArr, depth, cost, label = "0"):
        self.parent = parent_Node
        self.index = index
        self.stateStr = stateStr
        self.depth = depth
        self.cost = cost
        self.offset = size
        self.state_as_BinaryArr = np.empty(self.offset*self.offset, dtype=int)
        self.children = list()
        self.label = label
        self.fn = 0
        self.gn = 0
        self.hn = 0
           
        if(depth == 0):
            for i in range(len(self.state_as_BinaryArr)):
                self.state_as_BinaryArr[i] = int(self.stateStr[i])
            
        #print("maryam ****")
        #example = list()
        #temp1='101001001'
        #temp2='101001111'
        #temp3='111011001'
        #temp4='101101011'
        #temp5='111011111'
        #temp6=str(bin(2**100))

        #example.append(temp1)
        #example.append(temp2)
        #example.append(temp3)
        #example.append(temp4)
        #example.append(temp5)
        #example.append(temp6)

        #print(sorted(example , key = Node_BinaryRep.stringToDecimal ,reverse = True))
        #print(example)
        #print("maryam ****")
    
    @staticmethod
    def stringToDecimal(stateStr):
        str1 = str(stateStr)
        b = int(str1 ,2)
        return b
        
    def generateChildren(self):
       for i in range(len(self.state_as_BinaryArr)):
            arr = self.touchAndMoveBitwiseApproach(i)
            str = arr.tostring()
            childrenList.append(str)
       return childrenList
        

    def generateChildrenAlreadyOrdered(self):
        for i in range(len(self.state_as_BinaryArr)):
            row = i // self.offset
            col = i % self.offset
            arr = self.touchAndMoveBitwiseApproach(i)
            str1 = str(arr)
            print (str1)
            n = Node_BinaryRep(self, i,self.offset, str1 ,arr, self.depth + 1, self.cost + 1,Puzzle_Util.generateNodeLabel(row,col))
            self.children.append(n)
        self.children = sorted(self.children , key = attrgetter('stateStr') ,reverse = True)


    def goalStateTest(self ,size):
        zeros_arr = np.zeros(len(self.state_as_BinaryArr), dtype = 'int')
        return (np.array_equal(zeros_arr , self.state_as_BinaryArr))
    
    
    def touchAndMoveBitwiseApproach(self , digit):
        zeros_arr = np.zeros(len(self.state_as_BinaryArr), dtype = 'int')
        indexNeedToChange =self.getValidIndexNeedToChange(digit)
        
        for i in indexNeedToChange:
            zeros_arr[i] = 1
       
        result = np.bitwise_xor(zeros_arr , self.state_as_BinaryArr)
        return (result)
        

    def getValidIndexNeedToChange(self , digit):
        validIndexes = list() #order is top, bot , left , right
        if (digit >-1 and digit < len(self.state_as_BinaryArr) ):
            validIndexes.append(digit)
            if(digit-self.offset >=0):#top neighbours
                validIndexes.append(digit-self.offset)
        
            if( (digit%self.offset) != 0 ):#left neighbours
                validIndexes.append(digit-1)
        
            if(digit+self.offset <len(self.state_as_BinaryArr)):#bot neighbour
                validIndexes.append(digit+self.offset)

            if((digit+1)%self.offset != 0):#right neighbours
                 validIndexes.append(digit+1)
        return validIndexes

    def getNeighbours(self , digit):
        neighbours = [-1,-1,-1,-1] #order is top, bot , left , right
        if (digit >-1 and digit < len(self.state_as_BinaryArr) ):
            if(digit-self.offset >=0):#top neighbours
                neighbours[0]=self.state_as_BinaryArr[digit-self.offset]
        
            if( (digit%self.offset) != 0 ):#left neighbours
                neighbours[2]=self.state_as_BinaryArr[digit-1]
        
            if(digit+self.offset <len(self.state_as_BinaryArr)):#bot neighbour
                neighbours[1]=self.state_as_BinaryArr[digit+self.offset]

            if((digit+1)%self.offset != 0):#right neighbours
                 neighbours[3]=self.state_as_BinaryArr[digit+1]
        return neighbours
            
class Puzzle_Util:

    def __init__(self):
        pass

     # instance method to generate node labels
    @staticmethod
    def generateNodeLabel(row , col):

        label_str = "".join([Row_Label(row).name, str(col+1)])
        return(label_str)

    @staticmethod
    def printArray(arr):
        flat = np.ravel(arr)
        for i in flat:
            print(i,end =" ")
        print()

class Puzzle:
    #static data member that keeps track of puzzle number
    puzzleNumber = -1

    def __init__(self, data):
        Puzzle.puzzleNumber += 1
        self.size = int(data[0])
        self.maxDepth = int(data[1])
        self.maxLength = int(data[2])
        self.stateString = data[3]
        index = 0
        self.root = Node_BinaryRep(None,0,self.size,self.stateString,None,0,0)

        # initialize closed list and open list
        self.closedList = OrderedDict()
        self.openList = OrderedDict()

        # create empty solution path arrays, they will be filled backwards once the solution path is found
        self.solutionPathLabels = list()
        self.solutionPathStates = list()
    
    
    def isGoal(self,givenArray,size):
        goal = np.zeros(size*size)
        if  np.array_equal(goal,givenArray):
            return True
        else:
            return False

    
    def puzzleDFS(self, node):
        
        if(node.depth>=self.maxDepth):
            #pop next element in stack
            self.puzzleDFS(self.openList.popitem(last=True))
                
            #IF stack if EMPTY , print "No Solution"
            if not bool(self.openList):
                print('No Solution')
                self.printSearchPath(SearchType.DFS)
        
        elif (self.isGoal(node.stateStr,self.size)):
            self.createSolutionPath(node)
            self.printSolutionPath(SearchType.DFS)
            self.printSearchPath(SearchType.DFS)

        else:

            #add node.state to the CLOSED LIST // DEPENDS ON TEAM DECISION
            self.closedList[node.stateStr] = node

            #THEN generate the node's children
            node.generateChildrenAlreadyOrdered()
            #IF NODE children do not have have higher depth than maxdepth, add them to OPEN LIST
            for item in node.children:
                if (item.depth<self.maxDepth) and (item.stateStr not in self.closedList):
                    self.closedList[item.stateStr]=item

            #IF stack if EMPTY , print "No Solution"
            if not bool(self.openList):
                print('No Solution')
                self.printSearchPath(SearchType.DFS)
            else:
                #POP next element on the Stack and visit
                self.puzzleDFS(self.openList.popitem(last=True))

    def printSolutionPath(self, type):
        if type == SearchType.DFS:
            outputFileName = str(self.puzzleNumber) + "_dfs_solution.txt"
        elif type == SearchType.BFS:
            outputFileName = str(self.puzzleNumber) + "_bfs_solution.txt"
        elif type == SearchType.BFS:
            outputFileName = str(self.puzzleNumber) + "_astar_solution.txt"

        file = open(outputFileName, 'w')

        if self.solutionPathStates.size > 0:
            for i in range(len(self.solutionPathStates) - 1, -1, -1):
                outputString = self.solutionPathStates[i].label + "\t"
                for j in range(len(self.solutionPathStates[i].stateStr)):
                    outputString += self.solutionPathStates[i].stateStr[j] + " "
                outputString += "\n"
                file.write(outputString)
        else:
            file.write("No solution")

        file.close()

    def printSearchPath(self, type):
        if type == SearchType.DFS:
            outputFileName = str(self.puzzleNumber) + "_dfs_search.txt"
        elif type == SearchType.BFS:
            outputFileName = str(self.puzzleNumber) + "_bfs_search.txt"
        elif type == SearchType.BFS:
            outputFileName = str(self.puzzleNumber) + "_astar_search.txt"

        file = open(outputFileName, 'w')

        for key, value in self.closedList.items():
            outputString = str(value.fn) + " " + str(value.gn) + " " + str(value.hn) + " " + key + "\n"
            file.write(outputString)

        file.close()

    def createSolutionPath(self, node):
        n = node
        if n.parent:
            while(true):
                self.solutionPathStates.append(node)
                n = n.parent
                if not n.parent:
                    self.solutionPathStates.append(node)
                    break
                
        

#MAIN
fileName = sys.argv[1]
puzzleData = list()
with open(str(fileName)) as file:
    puzzleData = file.readlines()

for data in puzzleData:
    data = data.split()
    p = Puzzle(data)
    p.puzzleDFS(p.root)