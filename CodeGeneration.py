import SemanticCube
import sys
global operandStack
operandStack = []
global operatorStack
operatorStack = []

global conditionalCountStack
conditionalCountStack = []
global jumpStack
jumpStack = []

global cuadruples
cuadruples = []

#Operand arithmetic
invOpMap = {
         0: 'int',   
         1: 'float', 
         2: 'string',
         3: 'bool',  
}
temporal = 0
def GenerateCuadruple():
    op = operatorStack.pop()
    operand2 = operandStack.pop()
    operand1 = operandStack.pop()
    result = SemanticCube.SearchSemanticCube(op, operand1[0], operand2[0])

    if (result != -1):
        
        if(op != '='):
            global temporal
            temporal = temporal + 1
            cuadruples.append([op, operand1, operand2, (result, ('Temporal', temporal))])
            operandStack.append((result, ('Temporal', temporal))) #Second position would be the temporal name?
        else:
            cuadruples.append([op, operand1, None, operand2])
    else:
        print("Error: Cannot %s (%s, %s)" % (op, invOpMap[operand1[0]], invOpMap[operand2[0]]))
        sys.exit()


#Console output
def GenerateOutputCuadruple():
    cuadruples.append(['console', None, None, operandStack.pop()])


#Conditional and loops
#conditionalCountStack controls the elif positions in different levels
def AppendConditionalCountStack():
    conditionalCountStack.append(0)


def IncreaseConsitionalCountStack():
    conditionalCountStack[-1] += 1


#generates empty GotoF, appends position to jumpStack
def GenerateGotofCuadruple():
    operand = operandStack.pop()
    if (operand[0] != 3):
        print("Error: Conditionals only evaluate bool, not %s" % (invOpMap[operand[0]]))
        sys.exit()
    else:
        jumpStack.append(len(cuadruples))
        cuadruples.append(['GotoF', operand, None, None])


#generates full GotoT, pops and uses last position of jumpStack
def GenerateGototCuadruple():
    operand = operandStack.pop()
    if (operand[0] != 3):
        print("Error: Conditionals only evaluate bool, not %s" % (invOpMap[operand[0]]))
        sys.exit()
    else:
        cuadruples.append(['GotoT', operand, None, jumpStack.pop()])


#generates empty Goto, appends position to jumpStack
def GenerateGotoCuadruple():
    jumpStack.append(len(cuadruples))
    cuadruples.append(['Goto', None, None, None])


#completes info of the cuadruple in position jumpPos of the jumpStack
def CompleteCuadruple(jumpPos, cuadruplePos):
    cuadruples[jumpStack.pop(jumpPos)][3] = len(cuadruples) + cuadruplePos


#in conditionals, completes all the empty Goto from the elifs pending
def CompleteGotoCuadruples():
    while(conditionalCountStack[-1] > 0):
        CompleteCuadruple(-1, 0)
        conditionalCountStack[-1] -= 1
    conditionalCountStack.pop()


#adds current cuadruple position to the jumpStack
def AppendJump():
    jumpStack.append(len(cuadruples))


#generates a Goto by poping and using position jumpPos of the jumpStack
def GotoJump(jumpPos):
    cuadruples.append(['Goto', None, None, jumpStack.pop(jumpPos)])
