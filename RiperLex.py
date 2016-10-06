import ply.lex as lex

# Reserved words
reserved = {
    'main' : 'MAIN',
    'function' : 'FUNCTION',
    'void' : 'VOID',
    'int' : 'INTTYPE',
    'float' : 'FLOATTYPE',
    'string' : 'STRINGTYPE',
    'bool' : 'BOOLTYPE',
    'array' : 'ARRAY',
    'console' : 'CONSOLE',
    'input' : 'INPUT',
    'if' : 'IF',
    'elif' : 'ELIF',
    'else' : 'ELSE',
    'for' : 'FOR',
    'while' : 'WHILE',
    'do' : 'DO',
    'return' : 'RETURN',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'global' : 'GLOBAL'
}

# List of tokens
tokens = ['ID',
          'AND',
          'OR',
          'LESS',
          'GREATER',
          'DIFFERENT',
          'EQUALTO',
          'LESSEQUAL',
          'GREATEREQUAL',
          'FLOAT',
          'INT',
          'STRING'] + list(reserved.values())

literals = ['=', '+', '-', '*', '/', '{', '}', '(', ')', '[', ']', ':', ',', ';', '%']

# Rules for tokens
t_ignore = ' \t'
t_EQUALTO = r'=='
t_LESS = r'<'
t_GREATER = r'>'
t_DIFFERENT = r'!='
t_LESSEQUAL = r'<='
t_GREATEREQUAL = r'>='
t_AND = r'&&'
t_OR = r'\|\|'
t_FLOAT = r'[0-9]+\.[0-9]+'
t_INT = r'[0-9]+'
t_STRING = r'\".*\"'

# Lookup in case of reserved words
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling rule
# def t_error(t):
#     print("Lexer error %s" % t.value[0])
#     exit(-1)
#     t.lexer.skip(1)

def t_error(t):
    t.type = t.value[0]
    t.value = t.value[0]
    t.lexer.skip(1)
    print("Illegal character '%s'" % t.value[0])
    print(t.lexer.lineno)
    exit(-1)

# Build the lexer
lexer = lex.lex()