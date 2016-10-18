#To compile
#python RiperLex.py 
#python RiperPar.py test.riper

import ply.yacc as yacc
import sys
import RiperLex
import SemanticCube

# import the lexical tokens
tokens = RiperLex.tokens

# Global function and variable directory
global globalDirectory
globalDirectory = {}

# Local variable directory
global localDirectory
localDirectory = {}

global varValues
varValues = []
global expQueue
expQueue = []
global correctProgram
correctProgram = True


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
            print "ERROR, variable ", p[2], " has already been declared"
            global correctProgram
            correctProgram = False
        else:
            # print("Popping")
            # print(varValues)
            localDirectory[p[2]] = [currentType, varValues.pop(-1)]
            # print(varValues)
            #NEED TO CHECK IF TYPE AND THE VALUE ARE EQUAL FOR ASSIGN


# Grammar rule used when more than one variable is declared
def p_moreVar(p):
    '''moreVar : ',' ID '=' expression moreVar
               | '''
    if (len(p) > 1):
        global localDirectory
        if (p[2] in localDirectory or p[2] in globalDirectory):
            print "ERROR, variable ", p[2], " has already been declared"
            global correctProgram
            correctProgram = False
        else:
            localDirectory[p[2]] = [currentType, varValues.pop(-1)]
            #NEED TO CHECK IF TYPE AND THE VALUE ARE EQUAL FOR ASSIGN
  

# Grammar rulle used to match to one of the basic variable type declaration tokens
def p_type(p):
    '''type : INTTYPE
            | FLOATTYPE
            | STRINGTYPE
            | BOOLTYPE '''
    if (len(p) > 1):
        global currentType
        currentType = p[1]

# 
def p_arrays(p):
  '''arrays : firstArr moreArray '''

def p_firstArr(p):
  '''firstArr : type ID '[' INT ']' '=' '{' expression moreExp '}' '''
  if (len(p) > 1):
    # print(p[4], varValues)
    if (int(p[4]) != len(varValues)):
      print "ERROR, the size of array ", p[2], " is different from the amount of contents"
      global correctProgram
      correctProgram = False
    del varValues[:]

def p_moreExp(p):
  '''moreExp : ',' expression moreExp
    | '''
  

def p_moreArray(p):
  '''moreArray : ',' ID '[' INT ']' '=' '{' expression moreExp '}' moreArray
    | '''
  if (len(p) > 1):
    if (int(p[4]) != len(varValues)):
      print "ERROR, the size of array ", p[2], " is different from the amount of contents"
      global correctProgram
      correctProgram = False
    del varValues[:]
  

def p_function(p):
  '''function : FUNCTION funcType ID '(' par ')' '{' block RETURN returnType ';' '}' '''
  if (len(p) > 1):
    global localDirectory
    global currentFuncType
    global varValues
    globalDirectory[p[3]] = [currentFuncType]
    localDirectory = {}
    del varValues[:]
  

def p_funcType(p):
  '''funcType : INTTYPE
    | FLOATTYPE
    | STRINGTYPE
    | BOOLTYPE
    | VOID '''
  if (len(p) > 1):
    global currentFuncType
    currentFuncType = p[1]
  

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
    localDirectory[p[2]] = [currentType]
  

def p_morePar(p):
  '''morePar : ',' type ID morePar
    | '''
  if (len(p) > 1):
    global localDirectory
    localDirectory[p[2]] = [currentType]
  

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
    if (p[1] not in localDirectory):
      if (p[1] not in globalDirectory):
        print "ERROR, variable ", p[1], " has not been declared"
        global correctProgram
        correctProgram = False

def p_possibleArray(p):
  '''possibleArray : '[' exp ']'
    | '''
  

def p_conditional(p):
  '''conditional : IF '(' expression ')' '{' block '}' possibleElif possibleElse '''
  

def p_possibleElif(p):
  '''possibleElif : ELIF '(' expression ')' '{' block '}' possibleElif
    | '''
  

def p_possibleElse(p):
  '''possibleElse : ELSE '{' block '}' 
    | '''
  

def p_output(p):
  '''output : CONSOLE '(' expression ')' ';' '''
  

def p_loop(p):
  '''loop : for
    | while
    | doWhile '''
  

def p_for(p):
  '''for : FOR '('  expression ';' assign ')' '{' loopBlock '}' '''
  

def p_while(p):
  '''while : WHILE '(' expression ')' '{' loopBlock '}' '''
  

def p_doWhile(p):
  '''doWhile : DO '{' loopBlock '}' WHILE '(' expression ')' ';' '''
  

def p_expression(p):
  '''expression : higherExp possibleHigherExp'''
  if (len(p) > 1):
    del expQueue[:]
  

def p_possibleHigherExp(p):
  '''possibleHigherExp : possibleHigherExpOp higherExp
    | '''
  

def p_possibleHigherExpOp(p):
  '''possibleHigherExpOp : AND
    | OR '''
  if (len(p) > 1):
    expQueue.append(p[1])

def p_higherExp(p):
  '''higherExp : exp possibleExp'''
  # print(p[1])

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
  if (len(p) > 1):
    expQueue.append(p[1])
  
def p_exp(p):
      '''exp : possibleSign term possibleTerms'''
  

def p_possibleTerms(p):
  '''possibleTerms : possibleTermOp possibleSign term possibleTerms
    | '''

def p_possibleSign(p):
  '''possibleSign : '+'
  | '-' 
  | '''   

def p_possibleTermOp(p):
  '''possibleTermOp : '+'
  | '-' '''
  if (len(p) > 1):
    expQueue.append(p[1])
  print 

def p_term(p):
  '''term : factor possibleFactors'''
  

def p_possibleFactors(p):
  '''possibleFactors : possibleFactorOp factor possibleFactors
    | '''
  

def p_possibleFactorOp(p):
  '''possibleFactorOp : '*'
    | '/'
    | '%' '''
  if (len(p) > 1):
    expQueue.append(p[1])
  
  

def p_factor(p):
  '''factor : lPar expression rPar
              | data'''

def p_lPar(p):
  '''lPar : '(' '''
  if (len(p) > 1):
    expQueue.append(p[1])

def p_rPar(p):
  '''rPar : ')' '''
  if (len(p) > 1):
    expQueue.append(p[1])

  

def p_data(p):
  '''data : ID possibleIdCall
    | constant
    | input '''
  if (len(p) == 3):
    global localDirectory
    global globalDirectory
    if (p[1] not in localDirectory):
      if (p[1] not in globalDirectory):
        print "ERROR, variable ", p[1], " has not been declared"
        global correctProgram
        correctProgram = False
      else:
        varValues.append(p[1])
    else:
      varValues.append(p[1])
  

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
    | TRUE
    | FALSE
    | STRING'''
  if (len(p) > 1):
    varValues.append(p[1])
    expQueue.append(p[1])
  p[0] = p[1]

def p_input(p):
  '''input : INPUT '(' inputPar ')' '''  
  p[0] = ('INPUT', p[3])

def p_inputPar(p):
  '''inputPar : STRING 
                 |  '''
  if(len(p) > 1):    
    p[0] = p[1]
  else:
    p[0] = ''

def p_error(p):
      print('Syntax error in line %d token %s with value %s' % (p.lineno, p.type, p.value))

  # Build the parser
RiperParser = yacc.yacc()
if __name__ == '__main__':
    if (len(sys.argv) > 1):
        file = sys.argv[1]
        try:
            f = open(file,'r')
            data = f.read()
            f.close()
            if (RiperParser.parse(data, debug = False, tracking=True)):
              if(correctProgram):
                print ('This is a correct and complete Riper program');
                print globalDirectory
        except EOFError:
            print(EOFError)
    else:
        print('File missing')