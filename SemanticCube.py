from collections import defaultdict
operMap = {
            '+'         : 0,
            '-'         : 1,
            '*'         : 2,
            '/'         : 3,
            '%'         : 4,
            '='         : 5,
            '<'         : 6,
            '>'         : 7,
            '<='        : 8,
            '>='        : 9,
            '=='        : 10,
            }

semanticCube = {}
# Return -1 if not possible
semanticCube = defaultdict(lambda: -1, semanticCube)

# int _ int : _
# float _ float : _
# int _ float : _
# float _ int : _
for i in range(0,4):
    semanticCube[i,0,0] = 0
    semanticCube[i,1,1] = 1
    semanticCube[i,0,1] = 1
    semanticCube[i,1,0] = 1
# = a a : a
for i in range(0,4):
    semanticCube[5, i, i] = i

# = int float: int
semanticCube[5, 0, 1] = 0
semanticCube[5, 1, 0] = 1
# % is always integer
semanticCube[4,0,0] = 0
semanticCube[4,1,1] = 0
semanticCube[4,0,1] = 0
semanticCube[4,1,0] = 0

# "string1" + "string2" = "string1string2"
semanticCube[2,0,2] = 2

def SearchSemanticCube(operator, operandOne, operandTwo):
    return semanticCube[operMap[operator], operandOne, operandTwo];