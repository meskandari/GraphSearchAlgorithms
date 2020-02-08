import sys
import numpy as np
from operator import itemgetter, attrgetter
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
        self.offset = size
        self.state_as_BinaryArr = np.empty(self.offset*self.offset, dtype=int)
        self.children = list()
            
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
            arr = self.touchAndMoveBitwiseApproach(i)
            str1 = str(arr)
            print (str1)
            n = Node_BinaryRep(self, i,self.offset, str1 ,arr, self.depth + 1, self.cost + 1)
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
        test = Node_BinaryRep(None,0,3,data[3],None,0,0)
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

def myFn(s):
    return int(s,2)
example = list()
temp1='101001001'
temp2='101001111'
temp3='111011001'
temp4='101101011'
temp5='111011111'
temp6=str(bin(2**100))

example.append(temp1)
example.append(temp2)
example.append(temp3)
example.append(temp4)
example.append(temp5)
example.append(temp6)

print(sorted(example,key=Node_BinaryRep.stringToDecimal,reverse=True))