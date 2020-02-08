import sys
import numpy as np
from collections import OrderedDict 

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

    @staticmethod
    def printArray(arr):
        flat = np.ravel(arr)
        for i in flat:
            print(i,end =" ")
        print()



class Puzzle:
    def __init__(self, data):
        self.size = int(data[0])
        self.maxDepth = int(data[1])
        self.maxLength = int(data[2])
        self.stateString = data[3]

        index = 0
        self.root = Node(None, None, self.stateString, 1, 0)

        # initialize closed list and open list
        self.closedList = OrderedDict()
        self.openList = OrderedDict()

    
    
    
    def isGoal(self,givenArray,size):
        goal = np.zeros(size*size)
        if  np.array_equal(goal,givenArray):
            return True
        else:
            return False

    
    def puzzleDFS(self,Node):
        
        if(Node.depth>=self.maxDepth):
            #pop next element in stack
            puzzleDFS(self.openList.popitem(last=True))
                
            #IF stack if EMPTY , print "No Solution"
            if not bool(self.openList):
                print('No Solution')
                #CREATE _DFS_SEARCH.TXT // JASON CODE
        
        elif (self.isGoal(Node.statestr,self.size)):
            print("JASON CODE TBD")
            #print DFS solution.txt // JASON CODE

        else:

            #add Node.state to the CLOSED LIST // DEPENDS ON TEAM DECISION
            self.closedList[Node.statestr] = Node

            #THEN generate the Node's children
            Node.generateChildren(self.size)
            #IF NODE children do not have have higher depth than maxdepth, add them to OPEN LIST
            for item in Node.children:
                if (item.depth<self.maxDepth) and (item.statestr not in self.closedList):
                    closedList[item.statestr]=item

            #IF stack if EMPTY , print "No Solution"
            if not bool(self.openList):
                print('No Solution')
            
            #POP next element on the Stack and visit
            puzzleDFS(self.openList.popitem(last=True))











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