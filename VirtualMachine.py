#import Memory

def Execute(globalMemoryMap, globalDirectory, quadruples, cons):
    constantDirectory = {}
    for a,b in cons.items():
        constantDirectory[b] = a
    print constantDirectory
    print(globalDirectory)
    print globalMemoryMap
    #globalMemory = Memory(globalDirectory)
