from arduino import Arduino
import math


class Interpreter:
    def __init__(self):
        self.tokens = []                # Tokens separados do txt
        self.setupInstructions = []     # Instrucoes para SETUP
        self.instructions = []          # Instrucoes gerais
        self.methodsInstructions = []   # Instrucoes para dentro de funcoes/if/else
        self.device = Arduino()         # Dispositivo utilizado
        self.variableLogs = {}          # Historico de todas as variaveis criadas

    def _translate(self):
        def createVariable(varName):
            if (self.device.mem < self.device.max_mem):
                if (varName not in self.variableLogs.keys()):
                    reg = self.device.getRegister()
                    self.variableLogs[varName] = {}
                    self.variableLogs[varName]['reg'] = reg
                    self.variableLogs[varName]['mem'] = ""

        def saveVariableValue(varName, value):
            if (varName in self.variableLogs.keys()):
                if (self.variableLogs[varName]['reg'] == ""):
                    self.variableLogs[varName]['reg'] = self.device.getRegister(
                    )
                reg = self.variableLogs[varName]['reg']
                self.instructions.append(self.device.LDI(reg, value))
                self.device.setRegister(reg)
                saveVarInMem(varName)
            else:
                print("Esta variavel ainda nao foi instanciada!")
                exit(1)

        def copyRegisters(varName1, varName2):
            if (varName1 in self.variableLogs.keys() and varName2 in self.variableLogs.keys()):
                getVarInMem(varName1)
                getVarInMem(varName2)
                reg1 = self.variableLogs[varName1]['reg']
                reg2 = self.variableLogs[varName2]['reg']
                self.instructions.append(self.device.MOV(reg1, reg2))
                self.device.setRegister(reg1)
                self.variableLogs[varName2]['reg'] = ""
                saveVarInMem(varName1)
                self.device.removeRegister(reg2)
                self.instructions.append(self.device.CLR(reg2))
            else:
                print("Alguma variavel nao foi instanciada!")
                exit(1)

        def saveVarInMem(varName, registrador=None):
            variableMemory = self.variableLogs[varName]['mem']
            if (variableMemory == ""):
                variableMemory = self.device.mem
            self.variableLogs[varName]['mem'] = variableMemory
            if (registrador == None):
                reg = self.variableLogs[varName]['reg']
            else:
                reg = registrador
            self.instructions.append(self.device.STS(
                str(hex(variableMemory))[2:], reg))
            self.instructions.append(self.device.CLR(reg))
            self.device.removeRegister(reg)
            self.variableLogs[varName]['reg'] = ""
            # TODO: Ajustar OFFSET
            self.device.mem += 4

        def getVarInMem(varName):
            variableMemory = self.variableLogs[varName]["mem"]
            if (variableMemory == ""):
                return None
            self.variableLogs[varName]["reg"] = self.device.getRegister()
            reg = self.variableLogs[varName]["reg"]
            self.device.setRegister(reg)
            self.instructions.append(
                self.device.LDS(reg, str(hex(variableMemory))[2:]))
            # TODO: Ajustar OFFSET
            self.device.mem += 4

        def getHardwareSetup(index):
            pass

        def run():
            index = 0
            while index < len(self.tokens)-1:
                pastToken = self.tokens[index-1]
                currentToken = self.tokens[index]
                nextToken = self.tokens[index]

                if (index < len(self.tokens)-1):
                    nextToken = self.tokens[index+1]

                if (pastToken.type == "DATATYPE" and currentToken.type == "IDENTIFIER"):
                    createVariable(currentToken.value)

                if (currentToken.type == "HARDWARE SETUP"):
                    getHardwareSetup(index)

                if (currentToken.type == "KEYWORD"):
                    if (currentToken.value == "if"):
                        pass

                if (currentToken.type == "OPERATOR"):
                    if (currentToken.value == "="):
                        # Ler tudo para frente até ";"
                        # Verificar tamanho, se for 1, é apenas uma atribuição simples
                        # Se for mais de um, identificar quais são os operadores
                        # Fazer operações partindo do primeiro operador com o elemento anterior e o posterior
                        # Na proxima operação, pegar o resultado da operação anterior
                        elementsList = []
                        index += 1
                        while (self.tokens[index].type != "TERMINATOR"):
                            elementsList.append(self.tokens[index])
                            # print(elementsList)
                            index += 1

                        if (len(elementsList) != 1):
                            numberResult = 0
                            elementIndex = 0
                            while elementIndex != (len(elementsList) - 1):
                                if elementsList[elementIndex].value.isdigit() and (elementIndex + 2) < len(elementsList) and elementsList[elementIndex + 2].value.isdigit():
                                    arithOp = ""
                                    for i in range(3):
                                        arithOp += elementsList[elementIndex + i].value
                                    numberResult = math.floor(eval(arithOp))
                                    del elementsList[elementIndex:(
                                        elementIndex + 2)]
                                    elementsList[elementIndex].value = str(
                                        numberResult)
                                else:
                                    elementIndex += 1
                        for e in elementsList:
                            print(e.value)

                        if (len(elementsList) == 1):
                            nextToken = elementsList[0]
                            if (nextToken.value.isdigit()):
                                saveVariableValue(
                                    pastToken.value, nextToken.value)
                            elif (nextToken.value.isalpha()):
                                copyRegisters(pastToken.value, nextToken.value)
                        elif (len(elementsList) == 3):
                            arithOp = ""
                            opVar = ""
                            algorithmReg = self.device.getRegister()

                            for e in elementsList:
                                if e.value.isdigit():
                                    self.instructions.append(
                                        self.device.LDI(algorithmReg, e.value))
                                elif e.type == "ARITHMETIC OPERATOR":
                                    arithOp = e.value
                                else:
                                    opVar = e.value

                            firstReg = 0
                            secondReg = 0
                            getVarInMem(opVar)
                            if elementsList[0].value == opVar:
                                firstReg = self.variableLogs[opVar]['reg']
                                secondReg = algorithmReg
                            else:
                                firstReg = algorithmReg
                                secondReg = self.variableLogs[opVar]['reg']

                            print(arithOp)
                            print(opVar)
                            if (arithOp == "+"):
                                self.instructions.append(
                                    self.device.ADD(firstReg, secondReg))
                                saveVarInMem(pastToken.value, firstReg)
                            elif (arithOp == "-"):
                                self.instructions.append(
                                    self.device.SUB(firstReg, secondReg))
                                saveVarInMem(pastToken.value, firstReg)

                print(self.variableLogs)
                index += 1
            print(self.instructions)
        run()

    def add(self, datatype):
        self.tokens.append(datatype)

    def getCode(self, device):
        self.device = device
        self._translate()       # Cria lista de instructions
        code = "start:\n"
        for i in self.setupInstructions:
            code += f"  {i}\n"
        code += f"main:\n"
        for i in self.instructions:
            code += f"  {i}\n"
        for i in self.methodsInstructions:
            code += f"  {i}\n"
        return code
