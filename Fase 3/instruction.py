class Instruction:
    def __init__(self, datatype, value, scope_depth=0):
        self.type = datatype
        self.value = value
        self.scope_depth = scope_depth
