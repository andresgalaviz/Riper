import SemanticCube
import Settings
from Settings import *
import sys

# This is the main part for compilation, all quadruples are saved in here.
# This list is passed to the virtual machine for execution
global quadruples
quadruples = []

# Operand stack is used to keep track of operands for expression evaluation
global operandStack
operandStack = []

# Operator stack is used to keep track of binary and unary operators for expression evaluation
global operatorStack
operatorStack = []

# conditionalCountStack is used to keep track of how many contiguos conditionals we have
global conditionalCountStack
conditionalCountStack = []

# jumpStack is used to keep track of the quadruples that still need to be completed
global jumpStack
jumpStack = []

# parameterList keeps history of the list of parameters that have not yet assigned to a function
global parameterList
parameterList = []

# currentParameterList keeps track of the current parameters being passed to a function
global currentParameterList
currentParameterList = []

# GenerateExpQuadruple
# This creates an expression quadruple and verifies type match
# Quadruple signature: [operator, operandOne, OperandTwo, Result]
def GenerateExpQuadruple():
    operator = operatorStack.pop()
    operandTwo = operandStack.pop()
    operandOne = operandStack.pop()
    
    result = SemanticCube.SearchSemanticCube(operator, operandOne[0], operandTwo[0])
    if (result != -1):
        if(operator != '='):
            quadruples.append([operator, operandOne[1], operandTwo[1], Settings.memoryMap[1][1][result]])
            operandStack.append((result, Settings.memoryMap[1][1][result])) #Second position would be the temporal name?
            Settings.memoryMap[1][1][result] = Settings.memoryMap[1][1][result] + 1
        else:
            quadruples.append([operator, operandOne[1], None, operandTwo[1]])
    else:
        print("Error: Cannot %s (%s, %s)" % (operator, invOpMap[operandOne[0]], invOpMap[operandTwo[0]]))
        sys.exit()

# GenerateOutputQuadruple
# This creates a console output quadruple 
# Quadruple signature: [console, None, None, OutputOperand]
def GenerateOutputQuadruple():
    quadruples.append(['console', None, None, operandStack.pop()[1]])


# Conditional and loops
# conditionalCountStack controls the elif positions in different levels
def AppendConditionalCountStack():
    conditionalCountStack.append(0)

# IncreaseConsitionalCountStack
# Ricky comment this
def IncreaseConsitionalCountStack():
    conditionalCountStack[-1] += 1

# GenerateGotofQuadruple
# Generates empty GotoF, appends position to jumpStack
def GenerateGotofQuadruple():
    operand = operandStack.pop()
    
    if (operand[0] != 3):
        print("Error: Conditionals only evaluate bool, not %s" % (invOpMap[operand[0]]))
        sys.exit()
    else:
        jumpStack.append(len(quadruples))
        quadruples.append(['GotoF', operand[1], None, None])

# GenerateGototQuadruple
# Generates full GotoT, pops and uses last position of jumpStack
def GenerateGototQuadruple():
    operand = operandStack.pop()
    if (operand[0] != 3):
        print("Error: Conditionals only evaluate bool, not %s" % (invOpMap[operand[0]]))
        sys.exit()
    else:
        quadruples.append(['GotoT', operand[1], None, jumpStack.pop()])

# Generates empty Goto, appends position to jumpStack
def GenerateGotoQuadruple():
    jumpStack.append(len(quadruples))
    quadruples.append(['Goto', None, None, None])

# Generates empty Goto, appends position to jumpStack
def GenerateGotoMainQuadruple():
    jumpStack.append(len(quadruples))
    quadruples.append(['GotoMain', None, None, None])


# Completes info of the quadruple in position jumpPos of the jumpStack
def CompleteQuadruple(jumpPos, quadruplePos):
    quadruples[jumpStack.pop(jumpPos)][3] = len(quadruples) + quadruplePos


# In conditionals, completes all the empty Goto from the elifs pending
def CompleteGotoQuadruples():
    while(conditionalCountStack[-1] > 0):
        CompleteQuadruple(-1, 0)
        conditionalCountStack[-1] -= 1
    conditionalCountStack.pop()


# Adds current quadruple position to the jumpStack
def AppendJump():
    jumpStack.append(len(quadruples))


# Generates a Goto by poping and using position jumpPos of the jumpStack
def GotoJump(jumpPos):
    quadruples.append(['Goto', None, None, jumpStack.pop(jumpPos)])

# Generates the parameters into function quadruples
def GenerateParInQuadruple(parnum):
    operand = operandStack.pop()
    quadruples.append(['PARAMETER', operand, None, parnum])

def GenerateFuncCallQuadruples(functionName, functionSignatue, parameterList):
    print("Func Call: ", functionSignatue, parameterList)
    quadruples.append(['ERA', None, None, functionName])
    if(len(parameterList) != len(functionSignatue[4])):
        print("ERROR, invalid parameter count provided for function: %s" % functionName)
        sys.exit()
    for index, parameter in enumerate(parameterList):
        if(parameter[0] != functionSignatue[4][index]):
            print("ERROR, type mismatch for parameter %d in function %s" % (index + 1, functionName))
            sys.exit()
        quadruples.append(['PAR', index, None, parameter])
    quadruples.append(['GOSUB', None, None, functionSignatue[1]])
    quadruples.append(['=', functionSignatue[3], None, Settings.memoryMap[1][1][functionSignatue[0]]])
    Settings.memoryMap[1][1][functionSignatue[0]] = Settings.memoryMap[1][1][functionSignatue[0]] + 1

# Used to generate the last quadruple of the RIPER language, signals the VM to terminate execution
def GenerateReturnProcQuadruple(functionName):
    operand = operandStack.pop()
    print("Function signature",functionName,  Settings.globalDirectory.get(functionName))
    quadruples.append(['RETURN', operand, None, Settings.globalDirectory.get(functionName)[3]])

    

# Used to generate the last quadruple of the RIPER language, signals the VM to terminate execution
def GenerateEndProcQuadruple():
    quadruples.append(['RIP', None, None, None])
