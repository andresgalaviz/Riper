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
                   [3700, 7700, 11700, 15700]]

# Local variables and temporals
# Order: [0][0] LocalInt, [0][1] LocalFloat, [0][2] LocalStrings, [0][3] LocalBools
#        [1][0] TemporalInt, [1][1] TemporalFloat, [1][2] TemporalStrings, [1][3] TemporalBools 

localMemoryMap = [[1900, 5900, 9900, 13900],
                  [2800, 6800, 10800, 14800]]

resetMemoryMap = copy.deepcopy(localMemoryMap)

# Keeps track of all the constants encountered during compilation and their virtual direction
# This way we don't have to keep adding them
global constantDirectory
constantDirectory = {}

constantDirectory[1] = globalMemoryMap[1][0]
globalMemoryMap[1][0] = globalMemoryMap[1][0] + 1
constantDirectory[-1] = globalMemoryMap[1][0]
globalMemoryMap[1][0] = globalMemoryMap[1][0] + 1

memoryMap = [globalMemoryMap, localMemoryMap]
global insideFunction
insideFunction = 0
opMap = {
        'int'       : 0,
        'float'     : 1,
        'string'    : 2,
        'bool'      : 3,
        'void'      : 4
}

#Operand arithmetic
invOpMap = {
         0: 'int',   
         1: 'float', 
         2: 'string',
         3: 'bool',  
}

global operandStack
operandStack = []
global operatorStack
operatorStack = []

global conditionalCountStack
conditionalCountStack = []
global jumpStack
jumpStack = []

global quadruples
quadruples = []