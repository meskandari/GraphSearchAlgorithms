import sys
import numpy as np

# unused at the moment
class State:
    def __init__(self, M):
        self.state = M



# each node representation for DFS 
class Node_dfs:

    def __init__(self, p_label,size, stateSrt):
        self.parent_label = p_label
        self.size = size
        self.state_as_Matrix = np.empty([self.size, self.size], dtype=int)
        index = 0
        for i in range(len(self.state_as_Matrix)):
            for j in range(len(self.state_as_Matrix[i])):
                self.state_as_Matrix[i,j] = int(stateSrt[index])
                index += 1

    def goalStateTest(self ,size):
        b = np.zeros(shape = (size, size), dtype = 'int')
        return (np.array_equal(b , self.state_as_Matrix))
        
    

class Puzzle_Engine:
       
    # Initializer / Instance Attributes
    def __init__(self, data):
        self.size = int(data[0])
        self.maxDepth = int(data[1])
        self.maxLength = int(data[2])
        self.initialState = data[3]
        self.currentDepth = 1;
        self.closeList = list()
        self.initialNode = Node_dfs(str(0),self.size,data[3])
        self.openList = deque()
        self.openList.append(self.initialNode)
        bool1= self.initialNode.goalStateTest(self.size)

   
        

class Puzzle_Util:

    def __init__(self):
        pass

     # instance method to generate node labels
    @staticmethod
    def generateNodeLabel(row , col):
        label_str = "".join([Row_Label(row).name, str(col+1)])
        return(label_str)


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
    my_puzzle = Puzzle_Engine(data)
    print(p.getNeighbours(0, 0))