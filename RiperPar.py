#To compile
#python RiperLex.py 
#python RiperPar.py test.riper

import ply.yacc as yacc
import sys
import copy
import RiperLex
import CodeGeneration
from CodeGeneration import *
import Settings
from time import time
from VirtualMachine import *


# import the lexical tokens
tokens = RiperLex.tokens

# Global Riper code structure
def p_program(p):
    '''program : globalVarDeclar generateGotoMain functionDeclar main'''
    # This is a complete and correct program, generate the EndProc quadruple
    GenerateRIPQuadruple()

# Generates the first quadruple to the main function
def p_generateGotoMain(p):
    '''generateGotoMain : '''
    GenerateGotoMainQuadruple()

# Global variable declaration section
def p_globalVarDeclar(p):
    '''globalVarDeclar : initVarDeclar '''
    if (len(p) > 1):
        global localDirectory
        
        if (len(localDirectory) > 0):
            Settings.globalDirectory = localDirectory.copy()
            localDirectory = {}
        global globalTemporals 
        globalTemporals = memoryMap[1][1]


# Variable initialization section
def p_initVarDeclar(p):
    '''initVarDeclar : varDeclar initVarDeclar
                     | '''


# Function declaration section                   
def p_functionDeclar(p):
    '''functionDeclar : function functionDeclar
                      | '''

# Variable or array declaration statute
def p_varDeclar(p):
    '''varDeclar : vars ';'
                 | ARRAY arrays ';' '''
  

# Variable declaration statue
def p_vars(p):
    '''vars : type ID '=' expressionInput moreVar'''
    if (len(p) > 1):
        global localDirectory
        if (p[2] in localDirectory or p[2] in Settings.globalDirectory):
            print("ERROR, variable ", p[2], " has already been declared")
            sys.exit()
        else:
            localDirectory[p[2]] = (0, currentType, memoryMap[insideFunction[0]][0][currentType])
            operandStack.append((currentType, memoryMap[insideFunction[0]][0][currentType]))
            operatorStack.append(p[3])
            GenerateExpQuadruple()
            memoryMap[insideFunction[0]][0][currentType] = memoryMap[insideFunction[0]][0][currentType] + 1
            
            

# Grammar rule used when more than one variable is declared
def p_moreVar(p):
    '''moreVar : ',' ID '=' expressionInput moreVar
               | '''
    if (len(p) > 1):
        global localDirectory
        if (p[2] in localDirectory or p[2] in Settings.globalDirectory):
            global insideFunction
            if(insideFunction[0] or Settings.globalDirectory[p[2]][0] == 1):
                print("ERROR, variable ", p[2], " has already been declared")
                sys.exit()
        else:
            localDirectory[p[2]] = (0, currentType, memoryMap[insideFunction[0]][0][currentType])
            operandStack.append((currentType, memoryMap[insideFunction[0]][0][currentType]))
            operatorStack.append(p[3])
            GenerateExpQuadruple()
            memoryMap[insideFunction[0]][0][currentType] = memoryMap[insideFunction[0]][0][currentType] + 1
  

# Grammar rulle used to match to one of the basic variable type declaration tokens
def p_type(p):
    '''type : INTTYPE
            | FLOATTYPE
            | STRINGTYPE
            | BOOLTYPE '''
    if (len(p) > 1):
        global currentType
        currentType = opMap[p[1]]
    
# def p_moreExp(p):
#     '''moreExp : ',' expression sumExpCount moreExp
#         | '''

# def p_sumExpCount(p):
#     '''sumExpCount : '''
#     # global expCount
#     # expCount += 1

def p_moreArray(p):
    '''moreArray : nextArray moreArray
        | '''

def p_nextArray(p):
    '''nextArray :  ',' ID '[' INT ']' moreArrayDimensions '''
    # global expCount
    # if (int(p[4][1]) != expCount):
    #     print("ERROR, the size of array ", p[2], " is different from the amount of contents declared")
    #     sys.exit()
    # expCount = 0;
  
def p_function(p):
  '''function : FUNCTION funcType idStartFunction '(' par ')' '{' block '}' '''
  
  Settings.globalDirectory[p[3]][2] = [[i - j for i, j in zip(memoryMap[1][0], resetMemoryMap[0])], 
                              [i - j for i, j in zip(memoryMap[1][1], resetMemoryMap[1])]]
  
  global localDirectory
  global insideFunction

  if(CodeGeneration.currentFuncType < 4 and not CodeGeneration.foundReturn):
      print("Function %s with type %s does not have a return value" %(insideFunction[1], invOpMap[CodeGeneration.currentFuncType]))
      sys.exit()
  GenerateEndProcQuadruple()
  insideFunction = [0, '']
  localDirectory = {}
  

def p_funcType(p):
    '''funcType : INTTYPE
        | FLOATTYPE
        | STRINGTYPE
        | BOOLTYPE
        | VOID '''
    if (len(p) > 1):
        CodeGeneration.currentFuncType = opMap[p[1]]
  
def p_idStartFunction(p):
    '''idStartFunction : ID '''
    global localDirectory
    localDirectory = {}
    jumpStack.append(len(quadruples))
    
    Settings.memoryMap[1] = copy.deepcopy(resetMemoryMap)
    
    if(debugParser):
        print("Resetting memoryMap")
    
    global insideFunction
    Settings.globalDirectory[p[1]] = [CodeGeneration.currentFuncType, jumpStack.pop(), None, None, None]
    if(CodeGeneration.currentFuncType != 4):
        Settings.globalDirectory[p[1]][3] = memoryMap[0][0][CodeGeneration.currentFuncType]
        memoryMap[0][0][CodeGeneration.currentFuncType] = memoryMap[0][0][CodeGeneration.currentFuncType] + 1
    insideFunction = [1, p[1]]
    p[0] = p[1]
    

def p_returnType(p):
    '''returnType : RETURN expression ';' '''
    GenerateReturnProcQuadruple(insideFunction[1])
    CodeGeneration.foundReturn = True

def p_main(p):
    '''main : MAIN startMainFunction completeMainQuadruple '(' par ')' '{' blockMain '}' '''
    if (len(p) > 1):
        global localDirectory
        Settings.globalDirectory['main'][2] = [[i - j for i, j in zip(memoryMap[1][0], resetMemoryMap[0])], 
                                      [i - j for i, j in zip(memoryMap[1][1], resetMemoryMap[1])]]
        global functionParameterDeclaration
        Settings.globalDirectory['main'][4] = functionParameterDeclaration
        functionParameterDeclaration = []
        localDirectory = {}

def p_startMainFunction(p):
    '''startMainFunction : '''
    global localDirectory
    localDirectory = {}
    jumpStack.append(len(quadruples))
    global insideFunction
    insideFunction = [1, 'main']
    Settings.memoryMap[1] = copy.deepcopy(resetMemoryMap)
    
    if(debugParser):
        print("Resetting memoryMap")

# Empty production used to complete the first GOTO quadruple to main function
def p_completeMainQuadruple(p):
    '''completeMainQuadruple : '''
    Settings.globalDirectory['main'] = [-1, len(quadruples), None, None, None]
    CompleteQuadruple(0, 0)

def p_par(p):
    '''par : typeID morePar 
        | '''

    global functionParameterDeclaration
    Settings.globalDirectory[insideFunction[1]][4] = functionParameterDeclaration
    functionParameterDeclaration = []

def p_morePar(p):
    '''morePar : ',' typeID morePar
        | '''

def p_typeID(p):
    '''typeID : type ID'''
    global currentType
    global functionParameterDeclaration
    localDirectory[p[2]] = (0, currentType, Settings.memoryMap[insideFunction[0]][0][currentType])
    functionParameterDeclaration.append(currentType)
    # Save in inside local variables
    Settings.memoryMap[insideFunction[0]][0][currentType] = Settings.memoryMap[insideFunction[0]][0][currentType] + 1

def p_funcCall(p):
    '''funcCall : ID '(' verifyParameterStack parIn ')' '''
    global currentParameterList
    global parameterList
    # functype, funcStart, memoryNeeded
    matchedID = Settings.globalDirectory.get(p[1])
    if (matchedID is None):
        print("ERROR, variable ", p[1], " has not been declared")
        sys.exit()

    p[0] = GenerateFuncCallQuadruples(p[1], matchedID, currentParameterList)

    currentParameterList = []
    operatorStack.pop()
    if(parameterList):
        currentParameterList = parameterList.pop()
        print("Printing from parameter list", currentParameterList)

def p_verifyParameterStack(p):
    '''verifyParameterStack : '''
    global currentParameterList
    global parameterList
    operatorStack.append('(')
    if(currentParameterList):
        print("Saving currentParameterList")
        parameterList.append(currentParameterList)
        currentParameterList = []
    
def p_parIn(p):
    '''parIn : parameter moreParIn
        | '''
    

def p_moreParIn(p):
    '''moreParIn : ',' parameter moreParIn
        | '''

def p_parameter(p):
    '''parameter : expression'''
    global currentParameterList
    global parameterList
    
    parameter = operandStack.pop()
    currentParameterList.append(parameter)

def p_block(p):
    '''block : varDeclar block
        | assign block
        | conditional block
        | loop block
        | funcCall ';' block
        | output block
        | returnType block
        | '''


def p_blockMain(p):
    '''blockMain : varDeclar blockMain
        | assign blockMain
        | conditional blockMain
        | loop blockMain
        | funcCall ';' blockMain
        | output blockMain
        | ''' 

def p_loopBlock(p):
    '''loopBlock : assign loopBlock
        | conditional loopBlock
        | loop loopBlock
        | funcCall ';' loopBlock
        | output loopBlock
        | returnType loopBlock
        | '''
  

def p_assign(p):
    '''assign : possibleArray '=' expressionInput ';' '''
    if(isinstance(p[1],str)):
        global localDirectory
        
        matchedDataType = localDirectory.get(p[1])
        if (matchedDataType is None):
            matchedDataType = Settings.globalDirectory.get(p[1])
            if (matchedDataType is None):
                print("ERROR, variable ", p[1], " has not been declared")
                sys.exit()
            else:
                matchedDataType = (matchedDataType[1], matchedDataType[2])
        else:
            matchedDataType = (matchedDataType[1], matchedDataType[2])
        
        # Continue here
        print("matchedDataType[1] + p[2]", matchedDataType[1], p[2])
        operandStack.append(matchedDataType)
        operatorStack.append(p[2])
        GenerateExpQuadruple()
    else:
        operandStack.append(p[1])
        operatorStack.append('=*') 
        GenerateArrayAccessQuadruple()
    
def p_expressionInput(p):
    '''expressionInput : expression 
                       | input 
                       | array '''
    
def p_possibleArray(p):
    '''possibleArray : ID
                     | arrayAssign'''
    print("p[1]", p[1])
    p[0] = p[1]
    

def p_conditional(p):
    '''conditional : IF appendConditionalCountStack '(' gotofIfExpression ')' '{' block '}' possibleElif possibleElse completeGotoQuadruples '''


def p_appendConditionalCountStack(p):
    '''appendConditionalCountStack : '''
    AppendConditionalCountStack()


def p_gotofIfExpression(p):
    '''gotofIfExpression : expression '''
    IncreaseConsitionalCountStack()
    GenerateGotofQuadruple()


def p_possibleElif(p):
    '''possibleElif : ELIF '(' completeQuadruplePlus1 generateGoto gotofIfExpression ')' '{' block '}' possibleElif
        | '''


def p_completeQuadruplePlus1(p):
    ''' completeQuadruplePlus1 : '''
    CompleteQuadruple(-1, 1)


def p_completeGotoQuadruples(p):
    '''completeGotoQuadruples : '''
    CompleteGotoQuadruples()


def p_possibleElse(p):
    '''possibleElse : ELSE completeQuadruplePlus1 generateGoto '{' block '}' 
        | '''


def p_generateGoto(p):
    '''generateGoto : '''
    GenerateGotoQuadruple()


def p_output(p):
    '''output : CONSOLE '(' outputExpression possibleOutputExpressions ')' ';' '''


def p_outputExpression(p):
    '''outputExpression : expression '''
    GenerateOutputQuadruple()


def p_possibleOutputExpressions(p):
    '''possibleOutputExpressions : ',' outputExpression possibleOutputExpressions
    | '''
  

def p_loop(p):
    '''loop : for
        | while
        | doWhile '''
  

def p_for(p):
    '''for : FOR '(' appendJump gotofForExpression generateGoto ';' appendJump assign gotoJumpMinus4 ')' '{' completeQuadrupleJumpMinus2 loopBlock gotoJump completeQuadruple '}' '''


def p_completeQuadruple(p):
    '''completeQuadruple : '''
    CompleteQuadruple(-1, 0)


def p_gotofForExpression(p):
    '''gotofForExpression : expression'''
    GenerateGotofQuadruple()


def p_gotoJumpMinus4(p):
    '''gotoJumpMinus4 : '''
    GotoJump(-4)


def p_completeQuadrupleJumpMinus2(p):
    '''completeQuadrupleJumpMinus2 : '''
    CompleteQuadruple(-2, 0)


def p_while(p):
    '''while : WHILE '(' appendJump expression gotofWhileExpression ')' '{' loopBlock completeQuadruplePlus1 gotoJump '}' '''


def p_gotofWhileExpression(p):
    '''gotofWhileExpression : '''
    GenerateGotofQuadruple()


def p_gotoJump(p):
    '''gotoJump : '''
    GotoJump(-1)
  

def p_doWhile(p):
    '''doWhile : DO appendJump '{' loopBlock '}' WHILE '(' gototExpression ')' ';' '''


def p_appendJump(p):
    '''appendJump : '''
    AppendJump()


def p_gototExpression(p):
    '''gototExpression : expression '''
    GenerateGototQuadruple()


def p_expression(p):
    '''expression : higherExp1 possibleHigherExp1'''
    

def p_possibleHigherExp1(p):
    '''possibleHigherExp1 : operatorOR higherExp1 possibleHigherExp1
        | '''


def p_operatorOR(p):
    '''operatorOR : OR '''
    if(debugParser):
        print("PUSH ||")
    operatorStack.append(p[1])
  

def p_higherExp1(p):
    '''higherExp1 : higherExp2 possibleHigherExp2'''
    if (len(operatorStack) > 0 and operatorStack[-1] == '||'):
        if(debugParser):
            print("TOP " + operatorStack[-1] + ", GENERATING")
        GenerateExpQuadruple()


def p_possibleHigherExp2(p):
    '''possibleHigherExp2 : operatorAND higherExp2 possibleHigherExp2
        | '''


def p_operatorAND(p):
    '''operatorAND : AND '''
    if(debugParser):
        print("PUSH &&")
    operatorStack.append(p[1])


def p_higherExp2(p):
    '''higherExp2 : exp possibleExp'''
    if (len(operatorStack) > 0 and operatorStack[-1] == '&&'):
        if(debugParser):
            print("TOP " + operatorStack[-1] + ", GENERATING")
        GenerateExpQuadruple()


def p_possibleExp(p):
    '''possibleExp : possibleExpOp exp
        | '''
    

def p_possibleExpOp(p):
    '''possibleExpOp : LESS
        | GREATER
        | LESSEQUAL
        | GREATEREQUAL
        | DIFFERENT
        | EQUALTO '''
    if(debugParser):
        print("PUSHING", p[1])
    operatorStack.append(p[1])

  
def p_exp(p):
    '''exp : possibleSign term possibleTerms'''
    if (len(operatorStack) > 0 and operatorStack[-1] in ['<', '>', '<=', '>=', '!=', '==']):
        if(debugParser):
            print("TOP " + operatorStack[-1] + ", GENERATING")
        GenerateExpQuadruple()
  

def p_possibleTerms(p):
    '''possibleTerms : possibleTermOp possibleSign term possibleTerms
        | '''

def p_possibleSign(p):
    '''possibleSign : '+'
        | '-' 
        | '''   
    if(len(p) > 1):
        operatorStack.append('*')
        if(p[1] == '-'):
            operandStack.append((0, constantDirectory[-1]))
        else:
            operandStack.append((0, constantDirectory[1]))

def p_possibleTermOp(p):
    '''possibleTermOp : '+'
        | '-' '''
    if(debugParser):
        print("PUSHING", p[1])
    operatorStack.append(p[1])


def p_term(p):
    '''term : factor possibleFactors'''
    if (len(operatorStack) > 0 and operatorStack[-1] in ['+', '-', '+*']):
        if(debugParser):
            print("TOP +-, GENERATING")
        GenerateExpQuadruple()
  

def p_possibleFactors(p):
    '''possibleFactors : possibleFactorOp factor possibleFactors
        | '''
    if (len(p) == 1):
        p[0] = ''

def p_possibleFactorOp(p):
    '''possibleFactorOp : '*'
        | '/'
        | '%' '''
    p[0] = p[1]
    if(debugParser):
        print("PUSHING ", p[1])
    operatorStack.append(p[1])   
  
def p_factor(p):
    '''factor : lPar expression rPar
        | data'''
    if (len(p) == 2):
        p[0] = p[1]
        if (len(operatorStack) > 0 and operatorStack[-1] in ['*', '/', '%']):
            if(debugParser):
                print("TOP GENERATING ", operatorStack[-1])
            GenerateExpQuadruple()


def p_lPar(p):
    '''lPar : '(' '''
    if(debugParser):
        print("PUSH (")
    operatorStack.append(p[1])

def p_rPar(p):
    '''rPar : ')' '''
    if(debugParser):
        print("POP (")
    operatorStack.pop()
    if (len(operatorStack) > 0 and operatorStack[-1] in ['*', '/', '%']):
        GenerateExpQuadruple()

  

def p_data(p):
    '''data : constant
        | ID 
        | funcCall 
        | arrayAccess '''
    
    if(isinstance(p[1],str)):
        global localDirectory
        
        variableTuple = localDirectory.get(p[1])
        if (variableTuple is None):
            variableTuple = Settings.globalDirectory.get(p[1])
            if (variableTuple is None):
                print("ERROR, variable ", p[1], " has not been declared")
                sys.exit()
            elif(isinstance(variableTuple, list)):
                print(variableTuple)
                print("ERROR, ", p[1], " is a function")
                sys.exit()
            else:
                variableTuple = (variableTuple[1], variableTuple[2])
        
        else:
            variableTuple = (variableTuple[1], variableTuple[2])
    else: 
        variableTuple = p[1]
    
    # p[0] = p[1]
    if(debugParser):
        print("PUSHING OPERAND ", variableTuple)  
    print("variableTuple", variableTuple)
    operandStack.append(variableTuple)

# Used if more arrays are to be declared
def p_arrays(p):
    '''arrays : array moreArray '''

global R
R = 1

# Array grammar declaration
def p_array(p):
    '''array : type ID '[' calculateR moreArrayDimensions '''
    print(p[4])
    global R
    arraySize = R
    
    for idx in range(len(arrDimensions)):
        R = R/arrDimensions[idx][0]
        print R
        if(R not in constantDirectory):
            constantDirectory[R] = globalMemoryMap[1][0]
            globalMemoryMap[1][0] = globalMemoryMap[1][0] + 1
        
        arrDimensions[idx][1] = constantDirectory[R]
    
    global localDirectory
    if (p[2] in localDirectory or p[2] in Settings.globalDirectory):
        print("ERROR, variable ", p[2], " has already been declared")
        sys.exit()
    else:
        localDirectory[p[2]] = (0, currentType, memoryMap[insideFunction[0]][0][currentType], arrDimensions)
        print("memoryMap[insideFunction[0]][0][currentType]", memoryMap[insideFunction[0]][0][currentType])
        memoryMap[insideFunction[0]][0][currentType] = memoryMap[insideFunction[0]][0][currentType] + arraySize
        print("memoryMap[insideFunction[0]][0][currentType]", memoryMap[insideFunction[0]][0][currentType])

arrDimensions = []
def p_moreArrayDimensions(p):
    '''moreArrayDimensions : '[' calculateR moreArrayDimensions
                           | '''
    if(len(p) > 1):
        print(p[2])

def p_calculateR(p):
    '''calculateR : INT ']' '''
    global R
    global arrDimensions
    R = R * p[1][1]
    arrDimensions.append([p[1][1], None])

prevArrayDimensions = []

prevArraySignature = []
currentArraySignature = None

prevArraySums = []
currentArraySum = 0

def p_arrayAssign(p):
    '''arrayAssign : startArrayAccess '[' calculateAddress dimensionAccess '''
    
    operatorStack.pop()
    operatorStack.append('+*')
    operandStack.append((0, currentArraySignature[2]))
    
    GenerateExpQuadruple()
    p[0] = operandStack[-1]

    if(prevArrayDimensions):
        arrDimensions = prevArrayDimensions.pop()

def p_arrayAccess(p):
    '''arrayAccess : startArrayAccess '[' calculateAddress dimensionAccess '''
    
    operatorStack.pop()
    operatorStack.append('+*')
    operandStack.append((0, currentArraySignature[2]))
    
    GenerateExpQuadruple()
    operatorStack.append('=*')
    GenerateArrayAccessQuadruple()
    p[0] = operandStack[-1]

    if(prevArrayDimensions):
        arrDimensions = prevArrayDimensions.pop()


def p_startArrayAccess(p):
    '''startArrayAccess : ID '''
    global arrDimensions
    global prevArrayDimensions
    global prevArraySignature
    global currentArraySignature
    if(arrDimensions):
        prevArrayDimensions.append(arrDimensions)
        prevArraySignature.append(currentArraySignature)
        if(p[1] in localDirectory):
            currentArraySignature = localDirectory.get(p[1])
        elif(p[1] in Settings.globalDirectory):
            currentArraySignature = Settings.globalDirectory.get(p[1])
        else:
            print("ERROR, array variable ", p[1], " has not been declared")
            sys.exit()
        print("currentArraySignature", currentArraySignature)
        arrDimensions = 0
    operatorStack.append('(')
        
def p_calculateAddress(p):
    '''calculateAddress : expression ']' '''
    global arrDimensions
    global currentArraySum
    print("arrDimensions", currentArraySignature[3][arrDimensions][1])
    
    operatorStack.append('*')
    operandStack.append((0, currentArraySignature[3][arrDimensions][1]))
    print("operandStack", operandStack)
    GenerateExpQuadruple()
    if(arrDimensions > 0):
        operatorStack.append('+')
        GenerateExpQuadruple()
    
    arrDimensions = arrDimensions + 1

def p_dimensionAccess(p):
    '''dimensionAccess : '[' calculateAddress dimensionAccess
                       | '''



def p_constant(p):
    '''constant : INT
        | FLOAT
        | BOOL
        | STRING'''
    
    (constType, constValue) = p[1]
    if(constValue not in constantDirectory):
        constantDirectory[constValue] = globalMemoryMap[1][constType]
        globalMemoryMap[1][constType] = globalMemoryMap[1][constType] + 1
    p[0] = (constType, constantDirectory[constValue])
    


def p_input(p):
    '''input : INPUT '(' inputPar ')' '''  
    # TODO: This should not be hardcoded?
    p[0] = (0, 'INPUT', p[1])
    print("currentType", currentType)
    GenerateInputQuadruple(p[3][1], currentType)
    

def p_inputPar(p):
    '''inputPar : STRING 
        |  '''
    if(len(p) > 1):    
        p[0] = p[1]
    else:
        p[0] = ''

def p_error(p):
    print('Syntax error in line %d token %s with value %s' % (p.lineno, p.type, p.value))
    sys.exit()

  # Build the parser
RiperParser = yacc.yacc()
if __name__ == '__main__':
    if (len(sys.argv) > 1):
        file = sys.argv[1]
        try:
            f = open(file,'r')
            data = f.read()
            f.close()
            RiperParser.parse(data, debug = False, tracking=True)
            print('This is a correct and complete Riper program');
            quadrupleNumber = 0;
            print Settings.globalDirectory
            for quadruple in quadruples:
                print("%s \t %s" % (quadrupleNumber, quadruple))
                quadrupleNumber += 1
            print("OperandStack", operandStack)
            print("OperatorStack", operatorStack)
            print("globalDirectory", memoryMap)
            Execute(globalMemoryMap, globalTemporals, Settings.globalDirectory, quadruples, constantDirectory)

        except EOFError:
            print(EOFError)
    else:
        print('File missing')