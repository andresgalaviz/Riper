from Memory import *
import operator
from time import sleep
global ops
#ops is used for arithmetic operation, this was a cleaner approach than making a condition for every operator
ops = {
    "+" : operator.add,
    "+*" : operator.add,
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

    currentQuadruple = 0
    returnStack = []
    print("\nGLOBAL DIRECTORY\n")
    print(globalDirectory)
    #Initialize global memory required  
    globalMemoryMap.insert(1, globalTemporals)
    globalMemoryMap.insert(1, None)
    programMemory = Memory(globalMemoryMap)

    #Assign the constant values to the memory
    programMemory.assignConstants(constantDirectory)

    #Iterate through the quadruples
    print("\nSTART EXECUTION\n")
    while quadruples[currentQuadruple][0] != 'RIP':
        quadruple = quadruples[currentQuadruple]
             
        #Funtions
        #ERA: creates the memory of the function call
        if (quadruple[0] == 'ERA'):
            programMemory.assignFunctionMemory(globalDirectory[quadruple[3]][2])
            currentQuadruple += 1

        #PAR: sends parameters to new memory of function call
        elif (quadruple[0] == 'PAR'):
            programMemory.assignParameterToNewMemory(programMemory.getValueFromAddress(quadruple[3]), quadruple[3])
            currentQuadruple += 1

        #GOSUB: 'sleeps' current memory and assigns function call memory as current
        elif (quadruple[0] == 'GOSUB'):
            programMemory.switchToNewMemory()
            returnStack.append(currentQuadruple + 1)
            currentQuadruple = quadruple[3]

        #RETURN: saves the value to be returned, returns to quadruple after function call and wakes up memory
        elif (quadruple[0] == 'RETURN'):
            programMemory.assignValueToAddress(programMemory.getValueFromAddress(quadruple[1]), quadruple[3])
            currentQuadruple = returnStack.pop()
            programMemory.recoverMemory()

        #ENDPROC: returns to the quadruple after function call and wakes up memory
        elif (quadruple[0] == 'ENDPROC'):
            currentQuadruple = returnStack.pop()
            programMemory.recoverMemory()

        #GotoMain: After assigning any global variables, assigns main memory and goes to main quadruple
        elif (quadruple[0] == 'GotoMain'):
            #Initialize main function memory required to programMemory
            if(globalDirectory['main'][2] is not None):
                programMemory.assignMainMemory(globalDirectory['main'][2])
            currentQuadruple = quadruple[3]

        #Goto: goes to quadruple indicated
        elif (quadruple[0] == 'Goto'):
            currentQuadruple = quadruple[3]

        #GotoF: if false goes to quadruple indicated
        elif (quadruple[0] == 'GotoF'):
            if(not programMemory.getValueFromAddress(quadruple[1])):
                currentQuadruple = quadruple[3]
            else:
                currentQuadruple += 1

        #GotoT: if true goes to quadruple indicated
        elif (quadruple[0] == 'GotoT'):
            if(programMemory.getValueFromAddress(quadruple[1])):
                currentQuadruple = quadruple[3]
            else:
                currentQuadruple += 1

        #input: parses the input to the specified type and saves value to address
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

        #Console: prints value from address
        elif (quadruple[0] == 'console'):
            print programMemory.getValueFromAddress(quadruple[3])
            currentQuadruple += 1

        #Arithmetic: executes operation based on the operator received, saves resultant value to address
        elif (quadruple[0] in ['+', '-', '*', '/', '%', '<', '<=', '>', '>=', '==', '!=', '&&', '||']):
            programMemory.assignValueToAddress(ops[quadruple[0]](programMemory.getValueFromAddress(quadruple[1]), programMemory.getValueFromAddress(quadruple[2])), quadruple[3])
            currentQuadruple += 1
            
        #Arithmetic: executes operation based on the operator received, saves resultant value to address
        elif (quadruple[0] == '+*'):
            
            programMemory.assignValueToAddress(ops[quadruple[0]](programMemory.getValueFromAddress(quadruple[1]), quadruple[2]), quadruple[3])
            currentQuadruple += 1
        #Arithmetic: executes operation based on the operator received, saves resultant value to address
        elif (quadruple[0] == '=*'):
            print(quadruple, programMemory.getValueFromAddress(quadruple[1]))
            programMemory.assignValueToAddress(programMemory.getValueFromAddress(programMemory.getValueFromAddress(quadruple[1])), quadruple[3])
            currentQuadruple += 1
        #Assignation: assigns value to address
        elif(quadruple[0] == '='):
            print(quadruple, programMemory.getValueFromAddress(quadruple[3]))
            programMemory.assignValueToAddress(programMemory.getValueFromAddress(quadruple[1]), quadruple[3])
            print(quadruple, programMemory.getValueFromAddress(quadruple[3]))
            currentQuadruple += 1 
            
    print("\nFINISHED EXECUTION\n")
    print programMemory.memory



