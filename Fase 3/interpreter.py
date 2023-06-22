from arduino import Arduino
import math

pinout = {
    "B": ["8", "9", "10", "11", "12", "13", "-", "-"],
    "C": ["A0", "A1", "A2", "A3", "A4", "A5", "-", "-"],
    "D": ["0", "1", "2", "3", "4", "5", "6", "7"]
}


class Interpreter:
    def __init__(self):
        self.tokens = []                # Tokens separados do txt
        self.setupInstructions = []     # Instrucoes para SETUP
        self.instructions = []          # Instrucoes gerais
        self.device = Arduino()         # Dispositivo utilizado
        self.variableLogs = {}          # Historico de todas as variaveis criadas
        self.loopCounter = 0            # Contador de loops
        self.isInLoopContext = -1
        self.conditionsElements = []

    def _translate(self):
        def createVariable(varName):
            if (self.device.mem < self.device.max_mem):
                if (varName not in self.variableLogs.keys()):
                    reg = self.device.getRegister()
                    self.variableLogs[varName] = {}
                    self.variableLogs[varName]['reg'] = reg
                    self.variableLogs[varName]['mem'] = ""
                    self.variableLogs[varName]['value'] = ""

        def saveVariableValue(varName, value):
            if (varName in self.variableLogs.keys()):
                if (self.variableLogs[varName]['reg'] == ""):
                    self.variableLogs[varName]['reg'] = self.device.getRegister(
                    )
                reg = self.variableLogs[varName]['reg']
                self.instructions.append(self.device.LDI(reg, value))
                self.device.setRegister(reg)
                self.variableLogs[varName]['value'] = value
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

        def getHardware(index):
            if (self.tokens[index].value == "pinMode"):
                port = None
                bit = None
                value = self.tokens[index + 1].value
                # 0 - Input / 1 - Output
                direction = self.tokens[index + 3].value
                for k in list(pinout.keys()):
                    if (value in pinout[k]):
                        bit = pinout[k].index(value)
                        port = k
                        break
                if (port == None and bit == None):
                    print("Este pino nao existe")
                    exit(1)
                if (direction == "0"):
                    self.setupInstructions.append(
                        self.device.CBI(f"DDR{port}", bit))
                elif (direction == "1"):
                    self.setupInstructions.append(
                        self.device.SBI(f"DDR{port}", bit))
            if (self.tokens[index].value == "digitalWrite"):
                port = None
                bit = None
                value = self.tokens[index + 1].value
                # 0 - OFF / 1 - ON
                direction = self.tokens[index + 3].value
                for k in list(pinout.keys()):
                    if (value in pinout[k]):
                        bit = pinout[k].index(value)
                        port = k
                        break
                if (port == None and bit == None):
                    print("Este pino nao existe")
                    exit(1)
                if (direction == "0"):
                    self.instructions.append(
                        self.device.CBI(f"PIN{port}", bit))
                elif (direction == "1"):
                    self.instructions.append(
                        self.device.SBI(f"PIN{port}", bit))

        def run():
            index = 0
            while index < len(self.tokens)-1:
                pastToken = self.tokens[index-1]
                currentToken = self.tokens[index]
                nextToken = self.tokens[index]

                if (index < len(self.tokens)-1):
                    nextToken = self.tokens[index+1]

                if (currentToken.type == "CODE BLOCK STARTER"):
                    self.isInLoopContext += 1
                    print(self.isInLoopContext)

                if (currentToken.type == "CODE BLOCK FINISHER"):
                    nextLabel = "next_" + str(self.loopCounter) + ":"
                    self.isInLoopContext -= 1
                    print(self.isInLoopContext)

                    if (len(self.conditionsElements) == 1):
                        self.instructions.append(self.device.BRNE(
                            "next_" + str(self.loopCounter)))
                    else:
                        if (self.conditionsElements[1].value == '>'):
                            self.instructions.append(self.device.BRLE(
                                "next_" + str(self.loopCounter)))
                        elif (self.conditionsElements[1].value == '<'):
                            self.instructions.append(self.device.BRGE(
                                "next_" + str(self.loopCounter)))
                        elif (self.conditionsElements[1].value == '>='):
                            self.instructions.append(self.device.BRLO(
                                "next_" + str(self.loopCounter)))
                        elif (self.conditionsElements[1].value == '<='):
                            self.instructions.append(self.device.BRSH(
                                "next_" + str(self.loopCounter)))
                        elif (self.conditionsElements[1].value == '=='):
                            self.instructions.append(self.device.BRNE(
                                "next_" + str(self.loopCounter)))
                        elif (self.conditionsElements[1].value == '!='):
                            self.instructions.append(self.device.BREQ(
                                "next_" + str(self.loopCounter)))

                    self.instructions.append(self.device.RJMP(
                        "while_" + str(self.loopCounter)))
                    self.instructions.append(nextLabel)

                if (pastToken.type == "DATATYPE" and currentToken.type == "IDENTIFIER"):
                    createVariable(currentToken.value)

                if (currentToken.type == "HARDWARE SETUP" or currentToken.type == "HARDWARE INTERACTION"):
                    getHardware(index)

                if (currentToken.type == "KEYWORD"):
                    if (currentToken.value == "if"):
                        pass
                        # # Ler condição, começa em ( e termina )
                        # elementsList = []
                        # index += 2
                        # while (self.tokens[index].type != "FUNCTION ARGUMENT FINISHER"):
                        #     elementsList.append(self.tokens[index])
                        #     index += 1
                        # var1 = elementsList[0]
                        # var2 = elementsList[-1]
                        # comparison = elementsList[1:-1]
                        # comparisonText = "".join([e.value for e in comparison])
                        # # CPI
                        # if (comparisonText == ">="):
                        #     # ADD NAS INSTRUCOES O BGL
                        #     pass
                        # Criar novo código de bloco
                    elif (currentToken.value == "elseif"):
                        pass
                    elif (currentToken.value == "else"):
                        pass
                    elif (currentToken.value == "while"):
                        self.loopCounter += 1
                        contextName = "while_" + str(self.loopCounter) + ":"
                        index += 2
                        while (self.tokens[index].type != "FUNCTION ARGUMENT FINISHER"):
                            self.conditionsElements.append(self.tokens[index])
                            index += 1
                        index += 1

                        firstReg = self.device.getRegister()
                        secondReg = self.device.getRegister()
                        if (len(self.conditionsElements) == 1):
                            if (self.conditionsElements[0].value == "true"):
                                self.instructions.append(
                                    self.device.LDI(firstReg, 1))
                                self.instructions.append(
                                    self.device.LDI(secondReg, 1))
                            elif (self.conditionsElements[0].value == "false"):
                                self.instructions.append(
                                    self.device.LDI(firstReg, 1))
                                self.instructions.append(
                                    self.device.LDI(secondReg, 2))
                        else:
                            if (self.conditionsElements[0].value.isdigit()):
                                self.instructions.append(
                                    self.device.LDI(firstReg, self.conditionsElements[0].value))
                            else:
                                getVarInMem(self.conditionsElements[0].value)
                                firstReg = self.variableLogs[self.conditionsElements[0].value]['reg']

                            if (self.conditionsElements[2].value.isdigit()):
                                self.instructions.append(
                                    self.device.LDI(secondReg, self.conditionsElements[2].value))
                            else:
                                getVarInMem(self.conditionsElements[2].value)
                                firstReg = self.variableLogs[self.conditionsElements[2].value]['reg']

                        self.instructions.append(contextName)
                        self.instructions.append(
                            self.device.CP(firstReg, secondReg))

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
                            index += 1

                        if (len(elementsList) != 1):
                            numberResult = 0
                            elementIndex = 0
                            while elementIndex != (len(elementsList) - 1):
                                if (elementIndex + 2) < len(elementsList) and elementsList[elementIndex + 2].value.isdigit():
                                    arithOp = ""
                                    for i in range(3):
                                        if elementsList[elementIndex + i].value.isdigit():
                                            arithOp += elementsList[elementIndex + i].value
                                        elif elementsList[elementIndex + i].type == "ARITHMETIC OPERATOR":
                                            arithOp += elementsList[elementIndex + i].value
                                        else:
                                            arithOp += self.variableLogs[elementsList[elementIndex + i].value]['value']
                                    numberResult = math.floor(eval(arithOp))
                                    del elementsList[elementIndex:(
                                        elementIndex + 2)]
                                    elementsList[elementIndex].value = str(
                                        numberResult)

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
                            if (arithOp == "+"):
                                self.instructions.append(
                                    self.device.ADD(firstReg, secondReg))
                                saveVarInMem(pastToken.value, firstReg)
                            elif (arithOp == "-"):
                                self.instructions.append(
                                    self.device.SUB(firstReg, secondReg))
                                saveVarInMem(pastToken.value, firstReg)
                index += 1
        run()

    def add(self, datatype):
        self.tokens.append(datatype)

    def getCode(self, device):
        self.device = device
        self._translate()       # Cria lista de instructions
        code = "start:\n"
        for i in self.setupInstructions:
            code += f"{i}\n"
        code += f"main:\n"
        for i in self.instructions:
            code += f"{i}\n"
        return code
