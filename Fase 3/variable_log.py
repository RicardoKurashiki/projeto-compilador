class VariableLog:
    def __init__(self):
        self.variables = []
        self.verbose = False

    def toggleVerbose(self):
        self.verbose = not self.verbose
        print(f"VERBOSE > {self.verbose}")

    def add(self, varName, reg=None, mem=None):
        # Verificar se nao existe ja essa var
        variable = Variable(name=varName, reg=reg, mem=mem)
        self.variables.append(variable)
        if self.verbose:
            print(f"ADDED VARIABLE > {varName} | {reg} | {mem}")

    def hasVariable(self, varName):
        hasVar = False
        selectedVar = None
        for variable in self.variables:
            if variable.name == varName:
                hasVar = True
                selectedVar = variable
                break
        if self.verbose:
            print(f"HAS VARIABLE {varName} > {hasVar}")
        return hasVar, selectedVar

    def getReg(self, varName):
        # Verificar se o reg nao esta em uso
        hasVar, variable = self.hasVariable(varName)
        if not hasVar:
            if self.verbose:
                print(f"GET REG {varName} > DO NOT EXIST")
            return None
        if self.verbose:
            print(f"GET REG {varName} > {variable.reg}")
        return variable.reg

    def getMem(self, varName):
        hasVar, variable = self.hasVariable(varName)
        if not hasVar:
            if self.verbose:
                print(f"GET MEM {varName} > DO NOT EXIST")
            return None
        if self.verbose:
            print(f"GET MEM {varName} > {variable.address}")
        return variable.address

    def setReg(self, varName, reg):
        hasVar, variable = self.hasVariable(varName)
        if not hasVar:
            if self.verbose:
                print(f"SET REG {varName} > DO NOT EXIST")
            return False
        variable.setReg(reg)
        if self.verbose:
            print(f"SET REG {varName} > {reg}")
        return True

    def setMem(self, varName, mem):
        hasVar, variable = self.hasVariable(varName)
        if not hasVar:
            if self.verbose:
                print(f"SET MEM {varName} > DO NOT EXIST")
            return False
        variable.setMem(mem)
        if self.verbose:
            print(f"SET MEM {varName} > {mem}")
        return True

    def removeReg(self, varName):
        self.setReg(varName, None)

    def removeMem(self, varName):
        self.setMem(varName, None)

    def removeVar(self, varName):
        hasVar, variable = self.hasVariable(varName)
        if not hasVar:
            if self.verbose:
                print(f"REMOVE VAR {varName} > DO NOT EXIST")
            return False
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
    def __init__(self, name=None, reg=None, mem=None):
        self.name = name
        self.reg = reg
        self.address = mem

    def setReg(self, reg):
        self.reg = reg

    def setMem(self, mem):
        self.address = mem

    def toString(self):
        return f"VAR: {self.name} | REG: {self.reg} | MEM ADDRESS: {self.address}"
