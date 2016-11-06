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
        for scope in mainDirectory[0]:
            count += 1
            self.memory[count] = []
            for dataCount in scope:
                self.memory[count].append(dataCount * [None])

    def getValueFromAddress(self, virtualAddress):
        return self.memory[(virtualAddress - 1000) / 1000 % 4][(virtualAddress - 1000) / 4000][virtualAddress % 1000]

    def assignValueToAddress(self, result, virtualAddress):
        self.memory[(virtualAddress - 1000) / 1000 % 4][(virtualAddress - 1000) / 4000][virtualAddress % 1000] = result

            

        
