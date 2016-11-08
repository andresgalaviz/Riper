from Memory import *
import operator

global ops
ops = {
    "+" : operator.add,
    "-" : operator.sub,
    "*" : operator.mul,
    "/" : operator.div,
    "%" : operator.mod,
    "&&" : operator.and_,
    "||" : operator.or_,
    "==": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge
}


def Execute(globalMemoryMap, globalTemporals, globalDirectory, quadruples, constantDirectory):
    print("\nEXECUTING CODE\n")

    memoryStack = []
    currentQuadruple = 0

    print(globalDirectory)
    #Initialize global memory required     
    globalMemoryMap.append(globalTemporals)
    programMemory = Memory(globalMemoryMap)

    #Assign the constant values to the memory
    programMemory.assignConstants(constantDirectory)

    #Iterate through the quadruples
    print("\nSTART EXECUTION\n")
    while quadruples[currentQuadruple][0] != 'RIP':
        quadruple = quadruples[currentQuadruple]

        #GotoMain
        if (quadruple[0] == 'GotoMain'):
            #Initialize main function memory required to programMemory
            programMemory.assignMainMemory(globalDirectory['main'][2:4])
            currentQuadruple = quadruple[3]

        #Goto
        elif (quadruple[0] == 'Goto'):
            currentQuadruple = quadruple[3]

        #GotoF
        elif (quadruple[0] == 'GotoF'):
            if(not programMemory.getValueFromAddress(quadruple[1])):
                currentQuadruple = quadruple[3]
            else:
                currentQuadruple += 1

        #GotoT
        elif (quadruple[0] == 'GotoT'):
            if(programMemory.getValueFromAddress(quadruple[1])):
                currentQuadruple = quadruple[3]
            else:
                currentQuadruple += 1

        #Console
        elif (quadruple[0] == 'console'):
            print programMemory.getValueFromAddress(quadruple[3])
            currentQuadruple += 1

        #Arithmetic
        elif (quadruple[0] in ['+', '-', '*', '/', '%', '<', '<=', '>', '>=', '==', '!=', '&&', '||']):
            programMemory.assignValueToAddress(ops[quadruple[0]](programMemory.getValueFromAddress(quadruple[1]), programMemory.getValueFromAddress(quadruple[2])), quadruple[3])
            currentQuadruple += 1

        elif(quadruple[0] == '='):
            programMemory.assignValueToAddress(programMemory.getValueFromAddress(quadruple[1]), quadruple[3])
            currentQuadruple += 1
            
            
            
    print("\nFINISHED EXECUTION\n")
    print programMemory.memory



