#To compile
#python RiperLex.py 
#python RiperPar.py test.riper

import ply.yacc as yacc
import sys
import copy
import RiperLex
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
    GenerateEndProcQuadruple()

# Generates the first quadruple to the main function
def p_generateGotoMain(p):
    '''generateGotoMain : '''
    GenerateGotoMainQuadruple()

# Global variable declaration section
def p_globalVarDeclar(p):
    '''globalVarDeclar : initVarDeclar '''
    if (len(p) > 1):
        global localDirectory
        global globalDirectory
        if (len(localDirectory) > 0):
            globalDirectory = localDirectory.copy()
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
    '''vars : type ID '=' expression moreVar'''
    if (len(p) > 1):
        global localDirectory
        if (p[2] in localDirectory or p[2] in globalDirectory):
            print("ERROR, variable ", p[2], " has already been declared")
            sys.exit()
        else:
            localDirectory[p[2]] = [0, currentType, memoryMap[insideFunction][0][currentType]]
            operandStack.append((currentType, memoryMap[insideFunction][0][currentType]))
            operatorStack.append(p[3])
            GenerateExpQuadruple()
            memoryMap[insideFunction][0][currentType] = memoryMap[insideFunction][0][currentType] + 1
            
            

# Grammar rule used when more than one variable is declared
def p_moreVar(p):
    '''moreVar : ',' ID '=' expression moreVar
               | '''
    if (len(p) > 1):
        global localDirectory
        if (p[2] in localDirectory or p[2] in globalDirectory):
            global insideFunction
            if(insideFunction or globalDirectory[p[2]][0] == 1):
                print("ERROR, variable ", p[2], " has already been declared")
                sys.exit()
        else:
            localDirectory[p[2]] = [0, currentType, memoryMap[insideFunction][0][currentType]]
            operandStack.append((currentType, memoryMap[insideFunction][0][currentType]))
            operatorStack.append(p[3])
            GenerateExpQuadruple()
            memoryMap[insideFunction][0][currentType] = memoryMap[insideFunction][0][currentType] + 1
  

# Grammar rulle used to match to one of the basic variable type declaration tokens
def p_type(p):
    '''type : INTTYPE
            | FLOATTYPE
            | STRINGTYPE
            | BOOLTYPE '''
    if (len(p) > 1):
        global currentType
        currentType = opMap[p[1]]

# Used if more arrays are to be declared
def p_arrays(p):
    '''arrays : array moreArray '''

# Array grammar declaration
def p_array(p):
    '''array : type ID '[' INT ']' '=' '{' expression sumExpCount moreExp '}' '''
    if (len(p) > 1):
        global expCount
        if (int(p[4][1]) != expCount):
            print("ERROR, the size of array ", p[2], " is different from the amount of contents declared")
            sys.exit()
        expCount = 0;

def p_moreExp(p):
    '''moreExp : ',' expression sumExpCount moreExp
        | '''

def p_sumExpCount(p):
    '''sumExpCount : '''
    global expCount
    expCount += 1

def p_moreArray(p):
    '''moreArray : nextArray moreArray
        | '''

def p_nextArray(p):
    '''nextArray :  ',' ID '[' INT ']' '=' '{' expression sumExpCount moreExp '}' '''
    global expCount
    if (int(p[4][1]) != expCount):
        print("ERROR, the size of array ", p[2], " is different from the amount of contents declared")
        sys.exit()
    expCount = 0;
  
def p_function(p):
  '''function : FUNCTION funcType idStartFunction '(' par ')' '{' block '}' '''
  
  globalDirectory[p[3]][2] = [[i - j for i, j in zip(memoryMap[1][0], resetMemoryMap[0])], 
                              [i - j for i, j in zip(memoryMap[1][1], resetMemoryMap[1])]]
  
  global localDirectory
  localDirectory = {}
  global insideFunction
  insideFunction = 0

def p_funcType(p):
    '''funcType : INTTYPE
        | FLOATTYPE
        | STRINGTYPE
        | BOOLTYPE
        | VOID '''
    if (len(p) > 1):
        global currentFuncType
        currentFuncType = opMap[p[1]]
  
def p_idStartFunction(p):
    '''idStartFunction : ID '''
    global localDirectory
    localDirectory = {}
    jumpStack.append(len(quadruples))
    
    Settings.memoryMap[1] = copy.deepcopy(resetMemoryMap)
    
    if(debugParser):
        print("Resetting memoryMap")
    
    global currentFuncType
    global insideFunction
    globalDirectory[p[1]] = [currentFuncType, jumpStack.pop(), None]
    insideFunction = 1
    p[0] = p[1]
    

def p_returnType(p):
    '''returnType : RETURN expression ';' '''
    GenerateReturnProcQuadruple()

def p_  (p):
    '''main : MAIN startMainFunction completeMainQuadruple '(' par ')' '{' blockMain '}' '''
    if (len(p) > 1):
        global localDirectory
        if (len(localDirectory) > 0):
            globalDirectory['main'][2] = [[i - j for i, j in zip(memoryMap[1][0], resetMemoryMap[0])], 
                                          [i - j for i, j in zip(memoryMap[1][1], resetMemoryMap[1])]]
            localDirectory = {}

def p_startMainFunction(p):
    '''startMainFunction : '''
    global localDirectory
    localDirectory = {}
    jumpStack.append(len(quadruples))
    global insideFunction
    insideFunction = 1
    Settings.memoryMap[1] = copy.deepcopy(resetMemoryMap)
    
    if(debugParser):
        print("Resetting memoryMap")

# Empty production used to complete the first GOTO quadruple to main function
def p_completeMainQuadruple(p):
    '''completeMainQuadruple : '''
    globalDirectory['main'] = [-1, len(quadruples), None]
    CompleteQuadruple(0, 0)

def p_par(p):
    '''par : typeID morePar 
        | '''

def p_morePar(p):
    '''morePar : ',' typeID morePar
        | '''

def p_typeID(p):
    '''typeID : type ID'''
    global currentType
    localDirectory[p[2]] = (0, currentType, Settings.memoryMap[insideFunction][0][currentType])
    
    # Save in inside local variables
    Settings.memoryMap[insideFunction][0][currentType] = Settings.memoryMap[insideFunction][0][currentType] + 1

def p_funcCall(p):
    '''funcCall : ID verifyParameterStack '(' parIn ')' '''

    global globalDirectory
    global currentParameterList
    global parameterList
    # functype, funcStart, memoryNeeded
    matchedID = globalDirectory.get(p[1])
    if (matchedID is None):
        print("ERROR, variable ", p[1], " has not been declared")
        sys.exit()
    
    p[0] = matchedID 
    print("Current parameter list: ", p[1], currentParameterList)
    if(parameterList):
        currentParameterList = parameterList.pop()
        currentParameterList.append(("MY FUNCTION CALL", p[1]))
    
    GenerateFuncCallQuadruples(p[1], matchedID)

def p_verifyParameterStack(p):
    '''verifyParameterStack : '''
    global currentParameterList
    if(currentParameterList):
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
    if(isinstance(parameter,tuple)):
        currentParameterList.append(parameter)
    else:
        operandStack.pop()

def p_block(p):
    '''block : varDeclar block
        | assign ';' block
        | conditional block
        | loop block
        | funcCall ';' block
        | output block
        | input block
        | returnType block
        | '''


def p_blockMain(p):
    '''blockMain : varDeclar blockMain
        | assign ';' blockMain
        | conditional blockMain
        | loop blockMain
        | funcCall ';' blockMain
        | output blockMain
        | input blockMain
        | ''' 

def p_loopBlock(p):
    '''loopBlock : assign ';' loopBlock
        | conditional loopBlock
        | loop loopBlock
        | funcCall ';' loopBlock
        | output loopBlock
        | input loopBlock
        | '''
  

def p_assign(p):
    '''assign : ID possibleArray '=' expression '''
    if (len(p) > 1):
        global localDirectory
        global globalDirectory
        matchedDataType = localDirectory.get(p[1])
        if (matchedDataType is None):
            matchedDataType = globalDirectory.get(p[1])
            if (matchedDataType is None):
                print("ERROR, variable ", p[1], " has not been declared")
                sys.exit()
            else:
                matchedDataType = (matchedDataType[1], matchedDataType[2])
        else:
            matchedDataType = (matchedDataType[1], matchedDataType[2])
        
        # Continue here
        
        operandStack.append(matchedDataType)
        operatorStack.append(p[3])
        GenerateExpQuadruple()

def p_possibleArray(p):
    '''possibleArray : '[' exp ']'
        | '''
  

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
    if (len(operatorStack) > 0 and operatorStack[-1] in ['+', '-']):
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
        | input '''
    
    if(isinstance(p[1],str)):
        global localDirectory
        global globalDirectory
        variableTuple = localDirectory.get(p[1])
        if (variableTuple is None):
            variableTuple = globalDirectory.get(p[1])
            if (variableTuple is None):
                print("ERROR, variable ", p[1], " has not been declared")
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
    operandStack.append(variableTuple)


def p_possibleIdCall(p):
    '''possibleIdCall : '[' expression ']'
        | '(' parIn ')'
        | '''
    
    if(len(p) == 4):
        p[0] = p[2]
    else:
        p[0] = None

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
    p[0] = (0, 'INPUT')
    

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
            print globalDirectory
            for quadruple in quadruples:
                print("%s \t %s" % (quadrupleNumber, quadruple))
                quadrupleNumber += 1
            print(globalMemoryMap, globalTemporals, globalDirectory, quadruples, constantDirectory)
            Execute(globalMemoryMap, globalTemporals, globalDirectory, quadruples, constantDirectory)

        except EOFError:
            print(EOFError)
    else:
        print('File missing')