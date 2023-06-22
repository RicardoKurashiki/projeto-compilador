from arduino import Arduino


class Interpreter:
    def __init__(self):
        self.tokens = []
        self.setupInstructions = []
        self.instructions = []
        self.device = Arduino()
        self.variableLogs = {}

    def _translate(self):
        def createVariable(name):
            if (self.device.mem < self.device.max_mem):
                if (name not in self.variableLogs.keys()):
                    reg = self.device.getRegister()
                    self.variableLogs[name] = {}
                    self.variableLogs[name]['reg'] = reg
                    self.variableLogs[name]['mem'] = ""

        def saveVariableValue(name, value):
            if (name in self.variableLogs.keys()):
                if (self.variableLogs[name]['reg'] == ""):
                    self.variableLogs[name]['reg'] = self.device.getRegister()
                reg = self.variableLogs[name]['reg']
                cmd = self.device.LDI(reg, value)
                self.instructions.append(cmd)
                self.device.setRegister(reg)
                saveVarInMem(name)
            else:
                print("Esta variavel ainda nao foi instanciada!")

        def copyRegisters(name1, name2):
            if (name1 in self.variableLogs.keys() and name2 in self.variableLogs.keys()):
                if (self.variableLogs[name1]['reg'] == ""):
                    self.variableLogs[name1]['reg'] = self.device.getRegister()
                if (self.variableLogs[name2]['reg'] == ""):
                    self.variableLogs[name2]['reg'] = self.device.getRegister()
                reg1 = self.variableLogs[name1]['reg']
                reg2 = self.variableLogs[name2]['reg']
                cmd = self.device.MOV(reg1, reg2)
                self.instructions.append(cmd)
                self.device.setRegister(reg1)
                self.variableLogs[name2]['reg'] = ""
                saveVarInMem(reg1)

        def saveVarInMem(name):
            variableMemory = self.variableLogs[name]['mem']
            if (variableMemory == ""):
                variableMemory = self.device.mem
            self.variableLogs[name]['mem'] = variableMemory
            reg = self.variableLogs[name]['reg']
            self.device.removeRegister(reg)
            self.instructions.append(self.device.STS(
                str(hex(variableMemory))[2:], reg))
            self.instructions.append(self.device.CLR(reg))
            self.variableLogs[name]['reg'] = ""
            self.device.mem += 2

        def run():
            for index in range(0, len(self.tokens)):
                pastToken = self.tokens[index-1]
                currentToken = self.tokens[index]
                nextToken = self.tokens[index]
                if (index < len(self.tokens)-1):
                    nextToken = self.tokens[index+1]
                if (pastToken.type == "DATATYPE" and currentToken.type == "IDENTIFIER"):
                    createVariable(currentToken.value)
                if (currentToken.type == "OPERATOR"):
                    if (currentToken.value == "="):
                        saveVariableValue(pastToken.value, nextToken.value)
                print(self.instructions)

        run()

    def add(self, datatype):
        self.tokens.append(datatype)

    def getCode(self, device):
        self.device = device
        self._translate()
        return ""
