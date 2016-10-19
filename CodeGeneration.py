import SemanticCube
import sys
global operandStack
operandStack = []
global operatorStack
operatorStack = []

global cuadruples
cuadruples = []
invOpMap = {
         0: 'int',   
         1: 'float', 
         2: 'string',
         3: 'bool',  
}
temporal = 1
def GenerateCuadruple():
    op = operatorStack.pop()
    operand2 = operandStack.pop()
    operand1 = operandStack.pop()
    print(op, operand2, operand1)
    result = SemanticCube.SearchSemanticCube(op, operand1[0], operand2[0])

    if (result != -1):
        
        if(op != '='):
            global temporal
            temporal = temporal + 1
            cuadruples.append([op, operand1, operand2, (result, ('Temporal', temporal))])
            operandStack.append((result, '')) #Second position would be the temporal name?
        else:
            cuadruples.append([op, operand1, None, operand2])
    else:
        print("Error: Cannot %s (%s, %s)" % (op, invOpMap[operand1[0]], invOpMap[operand2[0]]))
        sys.exit()