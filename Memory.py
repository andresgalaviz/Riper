import sys
import Settings
from time import sleep

#local copying the initial virtual memory map from Settings
global memorySettings
memorySettings = [[],[],[],[]]

for idx, x in enumerate(Settings.globalMemoryMap):
    for y in x:
        memorySettings[idx * 3].append(y)

for idx, x in enumerate(Settings.localMemoryMap):
    for y in x:
        memorySettings[idx + 1].append(y)

memorySettings[3][0] -= 2
memorySettings[3][3] -= 2

#Position of the first global variables, used to know the 0 offset
global firstPosition
firstPosition = Settings.globalMemoryMap[0][0]

#The size of each scope, e.g. from localInt to temporalInt
global scopeSize
scopeSize = Settings.localMemoryMap[0][0] - Settings.globalMemoryMap[0][0]

#The size of each variable type, it should be 4 times the scopeSize, meaning the 4 scopes (global, local, temporal, constant) per variable type
global varSize
varSize = 4 * scopeSize

#requiredMemory is [[globalDeclared],[constants],[globalTemporals]]
class Memory:
    def __init__(self, requiredMemory):
        global memorySettings
        #The memory of the program will be an array of 4 arrays, corresponding to: 
        #global declared,
        #local declared, 
        #temporal, 
        #constants
        #Each of those 4 will have another 4 arrays, which are the 4 data types
        self.memory = [[],[],[],[]]
        self.memoryStack = []
        for scopeId, scope in enumerate(requiredMemory):
            if (scope):
                for dataCountId, dataCount in enumerate(scope):
                    if(dataCount > memorySettings[scopeId][dataCountId] + scopeSize):
                        print("ERROR: Memory overflow, not enough space for ", Settings.invOpMap[dataCountId])
                        sys.exit()
                    elif(dataCount == memorySettings[scopeId][dataCountId] + scopeSize):
                         self.memory[(dataCount - firstPosition - 1) / scopeSize % 4].append((dataCount - memorySettings[scopeId][dataCountId]) * [None])        
                    else:
                        self.memory[(dataCount - firstPosition) / scopeSize % 4].append((dataCount - memorySettings[scopeId][dataCountId]) * [None])
                    #(dataCount - memorySettings[scopeId][dataCountId]) * [None]
                    #((dataCount - firstPosition) % scopeSize) * [None]

    def assignConstants(self, constantDirectory):
        for value,virtualAddress in constantDirectory.items():
            self.memory[(virtualAddress - firstPosition) / scopeSize % 4][(virtualAddress - firstPosition) / varSize][(virtualAddress - firstPosition) % scopeSize] = value
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
        #The 0 created in the first position will be the parameter position counter
        self.newMemory = [0,[],[]]
        count = 0
        for scope in functionDirectory:
            count += 1
            for dataCount in scope:
                self.newMemory[count].append(dataCount * [None])
            

    def assignParameterToNewMemory(self, result, virtualAddress):
        if (virtualAddress < Settings.globalMemoryMap[0][1]):
            result = int(result)
            pos = 0
        elif (virtualAddress < Settings.globalMemoryMap[0][2]):
            result = float(result)
            pos = 1
        elif(virtualAddress < Settings.globalMemoryMap[0][3]):
            pos = 2
        else:
            pos = 3
        #The 0 stored in the first
        self.newMemory[1][pos][self.newMemory[0]] = result
        self.newMemory[0] += 1

    def switchToNewMemory(self):
        self.memoryStack.append(self.memory[1])
        self.memoryStack.append(self.memory[2])
        self.memory[1] = self.newMemory[1]
        self.memory[2] = self.newMemory[2]
        self.newMemory =None

    def recoverMemory(self):
        self.memory[2] = self.memoryStack.pop()
        self.memory[1] = self.memoryStack.pop()



    def getValueFromAddress(self, virtualAddress):
        return self.memory[(virtualAddress - firstPosition) / scopeSize % 4][(virtualAddress - firstPosition) / varSize][(virtualAddress - firstPosition) % scopeSize]

    def assignValueToAddress(self, result, virtualAddress):
        global memorySettings
        if (virtualAddress < memorySettings[0][1]):
            result = int(result)
        elif (virtualAddress < memorySettings[0][2]):
            result = float(result)
        self.memory[(virtualAddress - firstPosition) / scopeSize % 4][(virtualAddress - firstPosition) / varSize][(virtualAddress - firstPosition) % scopeSize] = result
