import sys
#requiredMemory is [[globalDeclared],[constants],[globalTemporals]]
class Memory:
    def __init__(self, requiredMemory):
        #The memory of the program will be an array of 4 arrays, corresponding to: 
        #global declared,
        #local declared, 
        #temporal, 
        #constants
        #Each of those 4 will have another 4 arrays, which are the 4 data types
        self.memory = [[],[],[],[]]
        self.memoryStack = []
        for scope in requiredMemory:
            for dataCount in scope:
                self.memory[(dataCount - 1000) / 1000 % 4].append(((dataCount - 1000) % 1000) * [None])

    def assignConstants(self, constantDirectory):
        for value,virtualAddress in constantDirectory.items():
            self.memory[(virtualAddress - 1000) / 1000 % 4][(virtualAddress - 1000) / 4000][virtualAddress % 1000] = value
        self.memory[3][3][0] = True
        self.memory[3][3][1] = False

    def assignMainMemory(self, mainDirectory):
        count = 0
        for scope in mainDirectory:
            count += 1
            self.memory[count] = []
            for dataCount in scope:
                self.memory[count].append(dataCount * [None])

    def assignFunctionMemory(self, functionDirectory):
        self.newMemory = [0,[],[],None]
        count = 0
        for scope in functionDirectory:
            count += 1
            for dataCount in scope:
                self.newMemory[count].append(dataCount * [None])
            

    def assignParameterToNewMemory(self, result, virtualAddress):
        if (virtualAddress < 5000):
            result = int(result)
            pos = 0
        elif (virtualAddress < 9000):
            result = float(result)
            pos = 1
        elif(virtualAddress < 13000):
            pos = 2
        else:
            pos = 3
        self.newMemory[1][pos][self.newMemory[0]] = result
        self.newMemory[0] += 1

    def switchToNewMemory(self):
        self.memoryStack.append(self.memory[1])
        self.memoryStack.append(self.memory[2])
        self.memory[1] = self.newMemory[1]
        self.memory[2] = self.newMemory[2]

    def recoverMemory(self):
        self.memory[2] = self.memoryStack.pop()
        self.memory[1] = self.memoryStack.pop()



    def getValueFromAddress(self, virtualAddress):
        return self.memory[(virtualAddress - 1000) / 1000 % 4][(virtualAddress - 1000) / 4000][virtualAddress % 1000]

    def assignValueToAddress(self, result, virtualAddress):
        if (virtualAddress < 5000):
            result = int(result)
        elif (virtualAddress < 9000):
            result = float(result)

        self.memory[(virtualAddress - 1000) / 1000 % 4][(virtualAddress - 1000) / 4000][virtualAddress % 1000] = result

            

        
