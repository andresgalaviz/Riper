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

global currentFuncType
currentFuncType = -1

global currentType
currentType = -1

global foundReturn
foundReturn = False

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

# GenerateArrayAccessQuadruple
# Used to create the access quadruple for array indices 
# [operator, operand[1], None, Settings.memoryMap[1][1][0]]]
def GenerateArrayAccessQuadruple():
    operator = operatorStack.pop()
    operand = operandStack.pop()
    quadruples.append([operator, operand[1], None, Settings.memoryMap[1][1][0]])
    operandStack.append((0, Settings.memoryMap[1][1][0])) #Second position would be the temporal name?
    Settings.memoryMap[1][1][0] = Settings.memoryMap[1][1][0] + 1

# GenerateOutputQuadruple
# This creates a console output quadruple 
# Quadruple signature: [console, None, None, OutputOperand]
def GenerateOutputQuadruple():
    message = operandStack.pop()[1]
    if(message is None):
        print("Error: Cannot print a None value")
        sys.exit()
    quadruples.append(['console', None, None, message])


# Conditional and loops
# conditionalCountStack controls the elif positions in different levels
def AppendConditionalCountStack():
    conditionalCountStack.append(0)

# IncreaseConsitionalCountStack
# Used to increase the conditionCount for each elif
def IncreaseConsitionalCountStack():
    conditionalCountStack[-1] += 1

# GenerateGotofQuadruple
# Generates empty GotoF, appends position to jumpStack
# Quadruple signature: [GotoF, operand[1], None, None]
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
# Quadruple signature: [GotoT, operand[1], None, quadruplePosition]
def GenerateGototQuadruple():
    operand = operandStack.pop()
    if (operand[0] != 3):
        print("Error: Conditionals only evaluate bool, not %s" % (invOpMap[operand[0]]))
        sys.exit()
    else:
        quadruples.append(['GotoT', operand[1], None, jumpStack.pop()])

# GenerateGotoQuadruple
# Generates empty Goto, appends position to jumpStack
# Quadruple signature: [Goto, None, None, None]
def GenerateGotoQuadruple():
    jumpStack.append(len(quadruples))
    quadruples.append(['Goto', None, None, None])


# GenerateGotoMainQuadruple
# Generates empty GotoMain, appends position to jumpStack
# Quadruple signature: [GotoMain, None, None, None]
def GenerateGotoMainQuadruple():
    jumpStack.append(len(quadruples))
    quadruples.append(['GotoMain', None, None, None])


# CompleteQuadruple
# Completes info of the quadruple in position jumpPos of the jumpStack
def CompleteQuadruple(jumpPos, quadruplePos):
    quadruples[jumpStack.pop(jumpPos)][3] = len(quadruples) + quadruplePos


# CompleteGotoQuadruples
# In conditionals, completes all the empty Goto from the elifs pending
def CompleteGotoQuadruples():
    while(conditionalCountStack[-1] > 0):
        CompleteQuadruple(-1, 0)
        conditionalCountStack[-1] -= 1
    conditionalCountStack.pop()


# AppendJump
# Adds current quadruple position to the jumpStack
def AppendJump():
    jumpStack.append(len(quadruples))


# GotoJump
# Generates a Goto by poping and using position jumpPos of the jumpStack
def GotoJump(jumpPos):
    quadruples.append(['Goto', None, None, jumpStack.pop(jumpPos)])

# GenerateParInQuadruple
# Generates the parameters into function quadruples
# Quadruple signature: [PARAMETER, operand, None, parnum]
def GenerateParInQuadruple(parnum):
    operand = operandStack.pop()
    quadruples.append(['PARAMETER', operand, None, parnum])


# GenerateFuncCallQuadruples
# Generates the ERA, PAR and GOSUB quadruples, validating the arguments
def GenerateFuncCallQuadruples(functionName, functionSignatue, parameterList):
    quadruples.append(['ERA', None, None, functionName])
    if(len(parameterList) != len(functionSignatue[4])):
        print("ERROR, invalid parameter count provided for function: %s" % functionName)
        sys.exit()
    for index, parameter in enumerate(parameterList):
        if(parameter[0] != functionSignatue[4][index]):
            print("ERROR, type mismatch for parameter %d in function %s" % (index + 1, functionName))
            sys.exit()
        quadruples.append(['PAR', index, None, parameter[1]])
    quadruples.append(['GOSUB', None, None, functionSignatue[1]])

    if(functionSignatue[0] == 4):
        return (functionSignatue[0], None)
    else:
        quadruples.append(['=', functionSignatue[3], None, Settings.memoryMap[1][1][functionSignatue[0]]])
        Settings.memoryMap[1][1][functionSignatue[0]] = Settings.memoryMap[1][1][functionSignatue[0]] + 1
        return (functionSignatue[0], Settings.memoryMap[1][1][functionSignatue[0]] - 1)

# Used to generate the RETURN quadruple
def GenerateReturnProcQuadruple(functionName):
    operand = operandStack.pop()
    if(currentFuncType != operand[0]):
        print("ERROR, type mismatch for return value in function %s with type %s for return type %s" % 
             (functionName, invOpMap[currentFuncType], invOpMap[operand[0]]))
        sys.exit()
    quadruples.append(['RETURN', operand[1], None, Settings.globalDirectory.get(functionName)[3]])

# Used to generate ENDPROC quadruple
def GenerateEndProcQuadruple():
    quadruples.append(['ENDPROC', None, None, None])

# Used to generate the input quadruple when assigning to a variable, assumes we will introduce the same
# valuetype. This will be verified or terminated in execution
def GenerateInputQuadruple(message, inputType):
    quadruples.append(['INPUT', message, inputType, Settings.memoryMap[1][1][inputType]])
    operandStack.append((inputType, Settings.memoryMap[1][1][inputType]))
    Settings.memoryMap[1][1][inputType] = Settings.memoryMap[1][1][inputType] + 1
    
# Used to generate the last quadruple of the RIPER language, signals the VM to terminate execution
def GenerateRIPQuadruple():
    quadruples.append(['RIP', None, None, None])

