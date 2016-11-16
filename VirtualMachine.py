from Memory import *
import operator
from time import sleep

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

    currentQuadruple = 0
    returnStack = []
    print("\nGLOBAL DIRECTORY\n")
    print(globalDirectory)
    #Initialize global memory required     
    globalMemoryMap.append(globalTemporals)
    programMemory = Memory(globalMemoryMap)

    #Assign the constant values to the memory
    programMemory.assignConstants(constantDirectory)

    print programMemory.memory

    #Iterate through the quadruples
    print("\nSTART EXECUTION\n")
    while quadruples[currentQuadruple][0] != 'RIP':
        quadruple = quadruples[currentQuadruple]
        
        
        #Funtions
        #ERA
        if (quadruple[0] == 'ERA'):
            programMemory.assignFunctionMemory(globalDirectory[quadruple[3]][2])
            currentQuadruple += 1

        #PAR
        elif (quadruple[0] == 'PAR'):
            programMemory.assignParameterToNewMemory(programMemory.getValueFromAddress(quadruple[3]), quadruple[3])
            currentQuadruple += 1

        #GOSUB
        elif (quadruple[0] == 'GOSUB'):
            programMemory.switchToNewMemory()
            returnStack.append(currentQuadruple + 1)
            currentQuadruple = quadruple[3]

        #RETURN
        elif (quadruple[0] == 'RETURN'):
            programMemory.assignValueToAddress(programMemory.getValueFromAddress(quadruple[1]), quadruple[3])
            currentQuadruple = returnStack.pop()
            programMemory.recoverMemory()

        #ENDPROC
        elif (quadruple[0] == 'ENDPROC'):
            currentQuadruple = returnStack.pop()
            programMemory.recoverMemory()




        #GotoMain
        elif (quadruple[0] == 'GotoMain'):
            #Initialize main function memory required to programMemory
            if(globalDirectory['main'][2] is not None):
                programMemory.assignMainMemory(globalDirectory['main'][2])
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

        #input
        elif (quadruple[0] == 'INPUT'):
            value = quadruple[1]
            if(quadruple[2] == 0):
                try:
                    #Can not cast a STRING in float format directly to int, so double cast is used
                    value = int(float(value))
                except:
                    print("ERROR, the input can not be cast to int")
                    sys.exit()
            elif(quadruple[2] == 1):
                try:
                    value = float(value)
                except:
                    print("ERROR, the input can not be cast to float")
                    sys.exit()
            elif(quadruple[2] == 3):
                if (value == 'true' or value == 'false'):
                    value = value == 'true'
                else:
                    print("ERROR, the input can not be cast to bool")
                    sys.exit()
            programMemory.assignValueToAddress(value, quadruple[3])
            currentQuadruple += 1


        #Console
        elif (quadruple[0] == 'console'):
            print programMemory.getValueFromAddress(quadruple[3])
            currentQuadruple += 1

        #Arithmetic
        elif (quadruple[0] in ['+', '-', '*', '/', '%', '<', '<=', '>', '>=', '==', '!=', '&&', '||']):
            programMemory.assignValueToAddress(ops[quadruple[0]](programMemory.getValueFromAddress(quadruple[1]), programMemory.getValueFromAddress(quadruple[2])), quadruple[3])
            currentQuadruple += 1

        #Assignation
        elif(quadruple[0] == '='):
            programMemory.assignValueToAddress(programMemory.getValueFromAddress(quadruple[1]), quadruple[3])
            currentQuadruple += 1
            
            
            
    print("\nFINISHED EXECUTION\n")
    print programMemory.memory



