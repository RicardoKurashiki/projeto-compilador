class VariableLog:
    def __init__(self, device):
        self.variables = []
        self.verbose = False
        self.device = device

    def toggleVerbose(self):
        self.verbose = not self.verbose
        print(f"VERBOSE > {self.verbose}")

    def add(self, varName):
        # Verificar se nao existe ja essa var
        variable = Variable(name=varName)
        self.variables.append(variable)
        if self.verbose:
            print(f"ADDED VARIABLE > {varName}")
        self.setMem(varName)

    def getVariable(self, varName):
        hasVar = False
        selectedVar = None
        for variable in self.variables:
            if variable.name == varName:
                hasVar = True
                selectedVar = variable
                break
        if self.verbose:
            print(f"HAS VARIABLE {varName} > {hasVar}")
        return selectedVar

    def getMem(self, varName):
        variable = self.getVariable(varName)
        if self.verbose:
            print(f"GET MEM {varName} > {variable.address}")
        return variable.address

    def setMem(self, varName):
        variable = self.getVariable(varName)
        if (self.device.mem < self.device.max_mem):
            mem_hex = str(hex(self.device.mem))
            variable.setMem(mem_hex)
            self.device.mem += 4
            if self.verbose:
                print(f"SET MEM {varName} > {mem_hex}")
            return True
        print("Sem memória")
        exit(1)

    def removeMem(self, varName):
        self.setMem(varName, None)

    def removeVar(self, varName):
        variable = self.getVariable(varName)
        self.variables.remove(variable)
        if self.verbose:
            print(f"REMOVE VAR {varName} > TRUE")
        return True

    def printLog(self):
        print("== START VARIABLE LOG DEBUG ==")
        for var in self.variables:
            print(var.toString())
        print("== END OF VARIABLE LOG DEBUG ==")


class Variable:
    def __init__(self, name=None, mem=None):
        self.name = name
        self.address = mem

    def setMem(self, mem):
        self.address = mem

    def toString(self):
        return f"VAR: {self.name} | MEM ADDRESS: {self.address}"
