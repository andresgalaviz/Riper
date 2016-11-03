import Memory

def Execute(globalMemoryMap, globalDirectory, quadruples, cons):
    constantDirectory = {}
    for a,b in cons.items():
        constantDirectory[b] = a

    memoryStack = []
    currentQuadruple = 0

    print constantDirectory
    print(globalDirectory)
    print globalMemoryMap
    #globalRequiredMemory = {'int' : globalMemoryMap[0][0] - 1000, 'intTempt' : globalMemoryMap[1][0] - 3700, 
    #                        'float' : globalMemoryMap[0][1] - 5000, 'floatTemp' : globalMemoryMap[1][1] - 7700, 
    #                        'string' : globalMemoryMap[0][2] - 9000, 'stringTemp' : globalMemoryMap[1][2] - 11700, 
    #                        'bool' : globalMemoryMap[0][3] - 13000, 'boolTemp' : globalMemoryMap[1][3] - 15700}

    #GALABLITZ MANDARA GLOBALREQURIEDMEMORY CON TODO
    #Initialize global memory required
    globalMemory = Memory(globalRequiredMemory)
    #Initialize main function memory required
    mainMemory = Memory(globalDirectory['main'].THE_MEMORY_VARIABLE_COUNTS)

    #Iterate through the quadruples
    while quadruples[currentQuadruple][0] != 'RIP':
        quadruple = quadruples[currentQuadruple]

        #Goto
        if (quadruple[0] == 'Goto'):
            currentQuadruple = quadruple[3]

        #Arithmetic operators
        #Addition
        elif (quadruple[0] == '+'):
            

