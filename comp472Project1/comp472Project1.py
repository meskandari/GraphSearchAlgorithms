import sys
import numpy as np
from collections import OrderedDict 

# unused at the moment
class State:
    def __init__(self, state):
        self.state = state

class Node_BinaryRep:

    def __init__(self, parent_Node,index, size, stateStr,state_as_BinaryArr, depth, cost):
        self.parent = parent_Node
        self.index = index
        self.stateStr = stateStr
        self.depth = depth
        self.cost = cost
        self.children = list()
        self.state_as_BinaryArr = state_as_BinaryArr
    
        if(state_as_BinaryArr == None):
            self.state_as_BinaryArr = np.empty(len(self.stateStr), dtype = 'int')
            for i in range(len(stateStr)):
                self.state_as_BinaryArr[i] = int(self.stateStr[i])
        #n= self.getNeighbours(3)
        #b = self.touchAndMoveBitwiseApproach(3)
        
        #print("maryam ****")
       
        #print(self.state_as_BinaryArr)
        #self.generateChildren()
        #print(test2)
        #print("maryam ****")

                
    def generateChildren(self):
       for i in range(len(self.state_as_BinaryArr)):
            arr = self.touchAndMoveBitwiseApproach(i)
            str = arr.tostring()
            childrenList.append(str)
       return childrenList
        

    def generateChildrenAlreadyOrdered(self):
        for i in range(len(self.state_as_BinaryArr)):
            arr = self.touchAndMoveBitwiseApproach(i)
            str = arr.tostring()
            n = Node_BinaryRep(self, i,self.size, str,arr, self.depth + 1, self.cost + 1)
            childrenList.append(n)


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
            


class Node:
    def __init__(self, parent, index, state, depth, cost):
        self.parent = parent
        self.index = index
        self.state = state
        self.depth = depth
        self.cost = cost
        self.children = list()


    #def generateChildren(self, max):
    #    for i in range(max):
    #        if(i != self.index):
    #            s = np.array(self.state)
    #            coords = np.unravel_index(i, s.shape)
    #            s = Puzzle_Util.moveTouch(s, s.shape[0], coords[0], coords[1])
    #            # cost + 1 for now
    #            n = Node(self, i, s, self.depth + 1, self.cost + 1)
    #            self.children.append(n)

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
        test = Node_BinaryRep(None,0,self.size,self.stateString,None,0,0)
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

    
    def puzzleDFS(self,stateStr,Node):
        
        if(Node.depth>=self.maxDepth):
            #pop next element in stack
            puzzleDFS(self.openList.popitem(last=True))
                
            #IF stack if EMPTY , print "No Solution"
            if not bool(self.openList):
                print('No Solution')
                #CREATE _DFS_SEARCH.TXT // JASON CODE
        
        elif (self.isGoal(Node.stateStr,self.size)):
            print("JASON CODE TBD")
            #print DFS solution.txt // JASON CODE

        else:

            #add Node.state to the CLOSED LIST // DEPENDS ON TEAM DECISION
            self.closedList[Node.stateStr] = Node

            #THEN generate the Node's children
            Node.generateChildrenAlreadyOrdered(self.size)
            #IF NODE children do not have have higher depth than maxdepth, add them to OPEN LIST
            for item in Node.children:
                if (item.depth<self.maxDepth) and (item.stateStr not in self.closedList):
                    closedList[item.stateStr]=item

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

    #print("parent node is: ", p.root)
    #p.root.generateChildren(p.size * p.size)
    #for i in range(len(p.root.children)):
    #    print("child ", p.root.children[i], " of parent ", p.root.children[i].parent)

    #print("state of child 0: ")
    #print(p.root.children[0].state)
    #print("parent's state is: ")
    #print(p.root.children[0].parent.state)