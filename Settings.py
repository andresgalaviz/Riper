import copy

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


# VirtualDirection = Base + type. Global/Local/Temporal/Constant + int: 000, float: 900, string: 1800, bool: 2700
# e.g. temporal float = 12100  
baseMemoryMap = {
        'global'    : 0,
        'local'     : 1,
        'temporal'  : 2,
        'constant'  : 3
}

# Global variables/functions and constants
# Order: [0][0] GlobalInt, [0][1] GlobalFloat, [0][2] GlobalStrings, [0][3] GlobalBools
#        [1][0] ConstantInt, [1][1] ConstantFloat, [1][2] ConstantStrings, [1][3] ConstantBools (I think we don't need strings and bools)

globalMemoryMap = [[1000, 5000, 9000, 13000], 
                   [4000, 8000, 12000, 16000]]

# Local variables and temporals
# Order: [0][0] LocalInt, [0][1] LocalFloat, [0][2] LocalStrings, [0][3] LocalBools
#        [1][0] TemporalInt, [1][1] TemporalFloat, [1][2] TemporalStrings, [1][3] TemporalBools 

localMemoryMap = [[2000, 6000, 10000, 14000],
                  [3000, 7000, 11000, 15000]]

resetMemoryMap = copy.deepcopy(localMemoryMap)

# Keeps track of all the constants encountered during compilation and their virtual direction
# This way we don't have to keep adding them
global constantDirectory
constantDirectory = {}

# We initialize constants needed for a complete compilation(-1, 1, true, false)
constantDirectory[1] = globalMemoryMap[1][0]
globalMemoryMap[1][0] = globalMemoryMap[1][0] + 1
constantDirectory[-1] = globalMemoryMap[1][0]
globalMemoryMap[1][0] = globalMemoryMap[1][0] + 1
constantDirectory['true'] = globalMemoryMap[1][3]
globalMemoryMap[1][3] = globalMemoryMap[1][3] + 1
constantDirectory['false'] = globalMemoryMap[1][3]
globalMemoryMap[1][3] = globalMemoryMap[1][3] + 1

# This is used to access each memory map numerically without the need of a conditional 
# Used in conjunstion with the insideFunction 
memoryMap = [globalMemoryMap, localMemoryMap]
global insideFunction
insideFunction = [0, '']

# This is used whenever we need to map a type to its numeric representation
opMap = {
        'int'       : 0,
        'float'     : 1,
        'string'    : 2,
        'bool'      : 3,
        'void'      : 4
}

# This is used whenever we need to map a type numeric representation to its type
invOpMap = {
         0: 'int',   
         1: 'float', 
         2: 'string',
         3: 'bool',  
         4: 'void'
}
global functionParameterDeclaration
functionParameterDeclaration = []