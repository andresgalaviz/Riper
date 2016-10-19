import SemanticCube
global operandStack
operandStack = []
global operatorStack
operatorStack = []

global cuadruples
cuadruples = []

def GenerateCuadruple():
    op = operatorStack.pop()
    operand2 = operandStack.pop()
    operand1 = operandStack.pop()
    print(op, operand2, operand1)
    result = SemanticCube.SearchSemanticCube(op, operand1[0], operand2[0])

    if (result != -1):
        cuadruples.append([op, operand1, operand2, (result, '')])
        
        if(op != '='):
            operandStack.append((result, '')) #Second position would be the temporal name?
    else:
        print "ERROR, type mismatch"