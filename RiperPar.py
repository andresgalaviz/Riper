#To compile
#python RiperLex.py 
#python RiperPar.py test.riper

import ply.yacc as yacc
import sys
import RiperLex
from CodeGeneration import * 

# import the lexical tokens
tokens = RiperLex.tokens

# Global function and variable directory
global globalDirectory
globalDirectory = {}

# Local variable directory
global localDirectory
localDirectory = {}
debugParser = False
#Counter of expressions in arrays
global expCount
expCount = 0;

opMap = {
        'int'       : 0,
        'float'     : 1,
        'string'    : 2,
        'bool'      : 3,
        'void'      : 4
}

# Global Riper code structure
def p_program(p):
    '''program : globalVarDeclar functionDeclar main'''
    p[0] = 'OK'  


# Global variable declaration section
def p_globalVarDeclar(p):
    '''globalVarDeclar : initVarDeclar '''
    if (len(p) > 1):
        global localDirectory
        global globalDirectory
        if (len(localDirectory) > 0):
            globalDirectory = localDirectory.copy()
            localDirectory = {}


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
            localDirectory[p[2]] = currentType
            operandStack.append((currentType, p[2]))
            operatorStack.append(p[3])
            GenerateCuadruple()
            
            

# Grammar rule used when more than one variable is declared
def p_moreVar(p):
    '''moreVar : ',' ID '=' expression moreVar
               | '''
    if (len(p) > 1):
        global localDirectory
        if (p[2] in localDirectory or p[2] in globalDirectory):
            print("ERROR, variable ", p[2], " has already been declared")
            sys.exit()
        else:
            localDirectory[p[2]] = currentType
            operandStack.append((currentType, p[2]))
            operatorStack.append(p[3])
            GenerateCuadruple()
            
  

# Grammar rulle used to match to one of the basic variable type declaration tokens
def p_type(p):
    '''type : INTTYPE
            | FLOATTYPE
            | STRINGTYPE
            | BOOLTYPE '''
    if (len(p) > 1):
        global currentType
        currentType = opMap[p[1]]

# 
def p_arrays(p):
    '''arrays : array moreArray '''

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
  '''function : FUNCTION funcType ID '(' par ')' '{' block RETURN returnType ';' '}' '''
  if (len(p) > 1):
    global localDirectory
    global currentFuncType
    globalDirectory[p[3]] = currentFuncType
    localDirectory = {}
  

def p_funcType(p):
    '''funcType : INTTYPE
        | FLOATTYPE
        | STRINGTYPE
        | BOOLTYPE
        | VOID '''
    if (len(p) > 1):
        global currentFuncType
        currentFuncType = opMap[p[1]]
  

def p_returnType(p):
    '''returnType : expression
        | VOID '''
  

def p_main(p):
    '''main : MAIN '(' par ')' '{' block '}' '''
    if (len(p) > 1):
        global localDirectory
        if (len(localDirectory) > 0):
            globalDirectory['main'] = localDirectory
            localDirectory = {}
  

def p_par(p):
    '''par : type ID morePar
        | '''
    if (len(p) > 1):
        global localDirectory
        localDirectory[p[2]] = currentType
  

def p_morePar(p):
    '''morePar : ',' type ID morePar
        | '''
    if (len(p) > 1):
        global localDirectory
        localDirectory[p[2]] = currentType
  

def p_funcCall(p):
    '''funcCall : ID '(' parIn ')' '''
  

def p_parIn(p):
    '''parIn : expression moreParIn
        | '''
  

def p_moreParIn(p):
    '''moreParIn : ',' expression moreParIn 
        | '''
  

def p_block(p):
    '''block : varDeclar block
        | assign ';' block
        | conditional block
        | loop block
        | funcCall ';' block
        | output block
        | input block
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
        
        # Continue here
        operandStack.append((matchedDataType, p[1]))
        operatorStack.append(p[3])
        GenerateCuadruple()

def p_possibleArray(p):
    '''possibleArray : '[' exp ']'
        | '''
  

def p_conditional(p):
    '''conditional : IF appendConditionalCountStack '(' gotofIfExpression ')' '{' block '}' possibleElif possibleElse completeGotoCuadruples '''


def p_appendConditionalCountStack(p):
    '''appendConditionalCountStack : '''
    AppendConditionalCountStack()


def p_gotofIfExpression(p):
    '''gotofIfExpression : expression '''
    IncreaseConsitionalCountStack()
    GenerateGotofCuadruple()


def p_possibleElif(p):
    '''possibleElif : ELIF '(' completeCuadruplePlus1 generateGoto gotofIfExpression ')' '{' block '}' possibleElif
        | '''


def p_completeCuadruplePlus1(p):
    ''' completeCuadruplePlus1 : '''
    CompleteCuadruple(-1, 1)


def p_completeGotoCuadruples(p):
    '''completeGotoCuadruples : '''
    CompleteGotoCuadruples()


def p_possibleElse(p):
    '''possibleElse : ELSE completeCuadruplePlus1 generateGoto '{' block '}' 
        | '''


def p_generateGoto(p):
    '''generateGoto : '''
    GenerateGotoCuadruple()


def p_output(p):
    '''output : CONSOLE '(' outputExpression possibleOutputExpressions ')' ';' '''


def p_outputExpression(p):
    '''outputExpression : expression '''
    GenerateOutputCuadruple()


def p_possibleOutputExpressions(p):
    '''possibleOutputExpressions : ',' outputExpression possibleOutputExpressions
    | '''
  

def p_loop(p):
    '''loop : for
        | while
        | doWhile '''
  

def p_for(p):
    '''for : FOR '(' appendJump gotofForExpression generateGoto ';' appendJump assign gotoJumpMinus4 ')' '{' completeCuadrupleJumpMinus2 loopBlock gotoJump completeCuadruple '}' '''


def p_completeCuadruple(p):
    '''completeCuadruple : '''
    CompleteCuadruple(-1, 0)


def p_gotofForExpression(p):
    '''gotofForExpression : expression'''
    GenerateGotofCuadruple()


def p_gotoJumpMinus4(p):
    '''gotoJumpMinus4 : '''
    GotoJump(-4)


def p_completeCuadrupleJumpMinus2(p):
    '''completeCuadrupleJumpMinus2 : '''
    CompleteCuadruple(-2, 0)


def p_while(p):
    '''while : WHILE '(' appendJump expression gotofWhileExpression ')' '{' loopBlock completeCuadruplePlus1 gotoJump '}' '''


def p_gotofWhileExpression(p):
    '''gotofWhileExpression : '''
    GenerateGotofCuadruple()


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
    GenerateGototCuadruple()


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
        GenerateCuadruple()


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
        GenerateCuadruple()


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
        GenerateCuadruple()
  

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
            operandStack.append((0, -1))
        else:
            operandStack.append((0, 1))

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
        GenerateCuadruple()
  

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
            GenerateCuadruple()


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
        GenerateCuadruple()

  

def p_data(p):
    '''data : constant
        | ID possibleIdCall
        | input '''
    if (len(p) == 3):
        global localDirectory
        global globalDirectory
        matchedDataType = localDirectory.get(p[1])
        
        if (matchedDataType is None):
            matchedDataType = globalDirectory.get(p[1])
            if (matchedDataType is None):
                print("ERROR, variable ", p[1], " has not been declared")
                sys.exit()
        variableTuple = (matchedDataType, p[1])

        
    else:
        variableTuple = p[1]
        
    p[0] = p[1]
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
        p[0] = ''

def p_constant(p):
    '''constant : INT
        | FLOAT
        | BOOL
        | STRING'''
    
    p[0] = p[1]


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
            print(globalDirectory)
            cuadrupleNumber = 0;
            for cuadruple in cuadruples:
                print("%s \t %s" % (cuadrupleNumber, cuadruple))
                cuadrupleNumber += 1
        except EOFError:
            print(EOFError)
    else:
        print('File missing')