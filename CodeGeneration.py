import SemanticCube
import Settings
from Settings import *
import sys


def GenerateExpQuadruple():
    op = operatorStack.pop()
    operand2 = operandStack.pop()
    operand1 = operandStack.pop()
    
    result = SemanticCube.SearchSemanticCube(op, operand1[0], operand2[0])
    if (result != -1):
        if(op != '='):
            quadruples.append([op, operand1[1], operand2[1], Settings.memoryMap[1][1][result]])
            operandStack.append((result, Settings.memoryMap[1][1][result])) #Second position would be the temporal name?
            Settings.memoryMap[1][1][result] = Settings.memoryMap[1][1][result] + 1
        else:
            quadruples.append([op, operand1[1], None, operand2[1]])
    else:
        
        print("Error: Cannot %s (%s, %s)" % (op, invOpMap[operand1[0]], invOpMap[operand2[0]]))
        sys.exit()


#Console output
def GenerateOutputQuadruple():
    quadruples.append(['console', None, None, operandStack.pop()[1]])


#Conditional and loops
#conditionalCountStack controls the elif positions in different levels
def AppendConditionalCountStack():
    conditionalCountStack.append(0)


def IncreaseConsitionalCountStack():
    conditionalCountStack[-1] += 1


#generates empty GotoF, appends position to jumpStack
def GenerateGotofQuadruple():
    
    operand = operandStack.pop()
    
    if (operand[0] != 3):
        print("Error: Conditionals only evaluate bool, not %s" % (invOpMap[operand[0]]))
        sys.exit()
    else:
        jumpStack.append(len(quadruples))
        quadruples.append(['GotoF', operand[1], None, None])


#generates full GotoT, pops and uses last position of jumpStack
def GenerateGototQuadruple():
    operand = operandStack.pop()
    if (operand[0] != 3):
        print("Error: Conditionals only evaluate bool, not %s" % (invOpMap[operand[0]]))
        sys.exit()
    else:
        quadruples.append(['GotoT', operand, None, jumpStack.pop()])


#generates empty Goto, appends position to jumpStack
def GenerateGotoQuadruple():
    jumpStack.append(len(quadruples))
    quadruples.append(['Goto', None, None, None])

#generates empty Goto, appends position to jumpStack
def GenerateGotoMainQuadruple():
    jumpStack.append(len(quadruples))
    quadruples.append(['GotoMain', None, None, None])


#completes info of the quadruple in position jumpPos of the jumpStack
def CompleteQuadruple(jumpPos, quadruplePos):
    quadruples[jumpStack.pop(jumpPos)][3] = len(quadruples) + quadruplePos


#in conditionals, completes all the empty Goto from the elifs pending
def CompleteGotoQuadruples():
    while(conditionalCountStack[-1] > 0):
        CompleteQuadruple(-1, 0)
        conditionalCountStack[-1] -= 1
    conditionalCountStack.pop()


#adds current quadruple position to the jumpStack
def AppendJump():
    jumpStack.append(len(quadruples))


#generates a Goto by poping and using position jumpPos of the jumpStack
def GotoJump(jumpPos):
    quadruples.append(['Goto', None, None, jumpStack.pop(jumpPos)])

# Generates the parameters into function quadruples
def GenerateParInQuadruple(parnum):
    operand = operandStack.pop()
    quadruples.append(['PARAMETER', operand, None, parnum])

def GenerateFuncCallQuadruples(functionName, functionSignatue):
    
    quadruples.append(['ERA', None, None, functionName])
    quadruples.append(['GOSUB', None, None, functionSignatue[1]])
    
    operandStack.append((functionSignatue[0], Settings.memoryMap[1][1][functionSignatue[0]]))
    Settings.memoryMap[1][1][functionSignatue[0]] = Settings.memoryMap[1][1][functionSignatue[0]] + 1
    

# Used to generate the last quadruple of the RIPER language, signals the VM to terminate execution
def GenerateReturnProcQuadruple():
    operand = operandStack.pop()
    quadruples.append(['RETURN', None, None, operand])

# Used to generate the last quadruple of the RIPER language, signals the VM to terminate execution
def GenerateEndProcQuadruple():
    quadruples.append(['RIP', None, None, None])
