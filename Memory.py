class Memory:
    def __init__(self, requiredMemory):
        #8 empty positions are created, representing the 4 declared types and the 4 temporal types
        self.memory = []
        for a in requiredMemory:
            self.memory.append(a * [None])
        
