from collections import defaultdict
operMap = {
            'int'       : 0,
            'float'     : 1,
            'string'    : 2,
            'bool'      : 3,
            '+'         : 0,
            '-'         : 1,
            '*'         : 2,
            '/'         : 3,
            '%'         : 4}

semanticCube = {}
# Return -1 if not possible
semanticCube = defaultdict(lambda: -1, semanticCube)

# int _ int = _
# float _ float = _
# int _ float = _
# float _ int = _
for i in range(0,4):
    semanticCube[0,i,0] = 0
    semanticCube[1,i,1] = 1
    semanticCube[0,i,1] = 1
    semanticCube[1,i,0] = 1

# % is always integer
semanticCube[0,4,0] = 0
semanticCube[1,4,1] = 0
semanticCube[0,4,1] = 0
semanticCube[1,4,0] = 0

# "string1" + "string2" = "string1string2"
semanticCube[2,0,2] = 2

def SearchSemantic(operandOne, operator, operandTwo):
    return semanticCube[operMap[operandOne], operMap[operator], operMap[operandTwo]];