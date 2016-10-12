#To compile
#python RiperLex.py 
#python RiperPar.py test.riper

import ply.yacc as yacc
import sys
import RiperLex
import SemanticCube
# import the lexical tokens
tokens = RiperLex.tokens

directory = {}
global currentTable
currentTable = {}
global varValues
varValues = []
global expQueue
expQueue = []
global correctProgram
correctProgram = True

precedence = (
    ('left','+','-'),
    ('left','*','/', '%'),
    ('right','UMINUS'),
    )



# define grammar rules
def p_program(p):
  '''program : globalVarDeclar functionDeclar main'''
  p[0] = 'OK'  

def p_globalVarDeclar(p):
  '''globalVarDeclar : initVarDeclar '''
  if (len(p) > 1):
    global currentTable
    global directory
    if (len(currentTable) > 0):
      directory = currentTable.copy()
      currentTable = {}


def p_initVarDeclar(p):
  '''initVarDeclar : varDeclar initVarDeclar
                   | '''
def p_functionDeclar(p):
  '''functionDeclar : function functionDeclar
                    | '''

def p_varDeclar(p):
  '''varDeclar : vars ';'
    | ARRAY arrays ';' '''
  

def p_vars(p):
  '''vars : type ID '=' expression moreVar'''
  if (len(p) > 1):
    global currentTable
    if (p[2] in currentTable or p[2] in directory):
      print "ERROR, variable ", p[2], " has already been declared"
      global correctProgram
      correctProgram = False
    else:
      currentTable[p[2]] = [currentType, varValues.pop(-1)]
      #NEED TO CHECK IF TYPE AND THE VALUE ARE EQUAL FOR ASSIGN



def p_moreVar(p):
  '''moreVar : ',' ID '=' expression moreVar
    | '''
  if (len(p) > 1):
    global currentTable
    if (p[2] in currentTable or p[2] in directory):
      print "ERROR, variable ", p[2], " has already been declared"
      global correctProgram
      correctProgram = False
    else:
      currentTable[p[2]] = [currentType, varValues.pop(-1)]
      #NEED TO CHECK IF TYPE AND THE VALUE ARE EQUAL FOR ASSIGN
  

def p_type(p):
  '''type : INTTYPE
    | FLOATTYPE
    | STRINGTYPE
    | BOOLTYPE '''
  if (len(p) > 1):
    global currentType
    currentType = p[1]

  
def p_arrays(p):
  '''arrays : firstArr moreArray '''

def p_firstArr(p):
  '''firstArr : type ID '[' INT ']' '=' '{' expression moreExp '}' '''
  if (len(p) > 1):
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
    global currentTable
    global currentFuncType
    global varValues
    directory[p[3]] = [currentFuncType]
    currentTable = {}
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
    global currentTable
    if (len(currentTable) > 0):
      directory['main'] = currentTable
      currentTable = {}
  

def p_par(p):
  '''par : type ID morePar
         | '''
  if (len(p) > 1):
    global currentTable
    currentTable[p[2]] = [currentType]
  

def p_morePar(p):
  '''morePar : ',' type ID morePar
    | '''
  if (len(p) > 1):
    global currentTable
    currentTable[p[2]] = [currentType]
  

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
    global currentTable
    global directory
    if (p[1] not in currentTable):
      if (p[1] not in directory):
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
  print(p[1])

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

def p_exp_binop(p):
    '''exp : exp '+' exp
           | exp '-' exp
           | exp '*' exp
           | exp '/' exp
           | exp '%' exp'''
    # if p[2] == '+'  : p[0] = p[1] + p[3]
    # elif p[2] == '-': p[0] = p[1] - p[3]
    # elif p[2] == '*': p[0] = p[1] * p[3]
    # elif p[2] == '/': p[0] = p[1] / p[3]
    print p[0]

def p_exp_uminus(p):
    '''exp : '-' exp %prec UMINUS'''
    p[0] = -p[2]

def p_exp_group(p):
    '''exp : '(' exp ')' '''
    p[0] = p[2]

# def p_exp_data(p):
#     '''exp : INT
#            | FLOAT 
#            | TRUE
#            | FALSE
#            | STRING '''
#     t[0] = t[1]

def p_exp_data(p):
  '''exp : ID possibleIdCall
    | constant
    | input '''
  if (len(p) == 3):
    global currentTable
    global directory
    if (p[1] not in currentTable):
      if (p[1] not in directory):
        print "ERROR, variable ", p[1], " has not been declared"
        global correctProgram
        correctProgram = False
      else:
        varValues.append(p[1])
    else:
      varValues.append(p[1])
  p[0] = p[1]

# def p_exp(p):
#       '''exp : term possibleTerms'''
  

# def p_possibleTerms(p):
#   '''possibleTerms : possibleTermOp term possibleTerms
#     | '''
  

# def p_possibleTermOp(p):
#   '''possibleTermOp : '+'
#   | '-' '''
#   if (len(p) > 1):
#     expQueue.append(p[1])
#   print 

# def p_term(p):
#   '''term : factor possibleFactors'''
  

# def p_possibleFactors(p):
#   '''possibleFactors : possibleFactorOp factor possibleFactors
#     | '''
  

# def p_possibleFactorOp(p):
#   '''possibleFactorOp : '*'
#     | '/'
#     | '%' '''
#   if (len(p) > 1):
#     expQueue.append(p[1])

  

# def p_factor(p):
#   '''factor : lPar expression rPar
#     | data'''

# def p_lPar(p):
#   '''lPar : '(' '''
#   if (len(p) > 1):
#     expQueue.append(p[1])

# def p_rPar(p):
#   '''rPar : ')' '''
#   if (len(p) > 1):
#     expQueue.append(p[1])

  

# def p_data(p):
#   '''data : ID possibleIdCall
#     | constant
#     | input '''
#   if (len(p) == 3):
#     global currentTable
#     global directory
#     if (p[1] not in currentTable):
#       if (p[1] not in directory):
#         print "ERROR, variable ", p[1], " has not been declared"
#         global correctProgram
#         correctProgram = False
#       else:
#         varValues.append(p[1])
#     else:
#       varValues.append(p[1])
  

def p_possibleIdCall(p):
  '''possibleIdCall : '[' expression ']'
    | '(' parIn ')'
    | '''
  

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
  
def p_inputPar(p):
  '''inputPar : STRING 
                 |  '''

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
            if (RiperParser.parse(data, debug = True, tracking=True)):
              if(correctProgram):
                print ('This is a correct and complete Riper program');
                print directory
        except EOFError:
            print(EOFError)
    else:
        print('File missing')