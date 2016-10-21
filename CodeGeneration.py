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


def GenerateOutputCuadruple():
    cuadruples.append(['console', None, None, operandStack.pop()])


def AppendConditionalCountStack():
    conditionalCountStack.append(0)


def GenerateGotofCuadruple():
    operand = operandStack.pop()
    if (operand[0] != 3):
        print("Error: Conditionals only evaluate bool, not %s" % (invOpMap[operand[0]]))
        sys.exit()
    else:
        jumpStack.append(len(cuadruples))
        cuadruples.append(['GotoF', operand, None, None])
        conditionalCountStack[-1] += 1


def CompleteCuadruple(x):
    cuadruples[jumpStack.pop()][3] = len(cuadruples) + x


def GenerateGotoCuadruple():
    jumpStack.append(len(cuadruples))
    cuadruples.append(['Goto', None, None, None])


def CompleteGotoCuadruples():
    while(conditionalCountStack[-1] > 0):
        CompleteCuadruple(0)
        conditionalCountStack[-1] -= 1
    conditionalCountStack.pop()