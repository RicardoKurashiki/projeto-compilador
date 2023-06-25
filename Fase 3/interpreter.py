from arduino import Arduino
from variable_log import VariableLog
from code import Code

class Interpreter:
    def __init__(self):
        self.tokens = []                # Tokens separados do txt
        self.device = Arduino()
        self.varLog = VariableLog(self.device)
        self.counter = Counter()
        self.code = Code()

    # == Funcoes Aux == #

    def loadConditions(self, firstTerm, secondTerm = None):
        outputInstructions = []
        firstTermReg = self.device.getRegister()
        secondTermReg = self.device.getRegister()

        if (firstTerm == "true"):
            # Carrega número no registrador 1
            outputInstructions.append(self.device.LDI(firstTermReg, "1"))
            # Carrega número no registrador 2
            outputInstructions.append(
                self.device.LDI(secondTermReg, "1"))
            # Realiza a comparação
            outputInstructions.append(
                self.device.CP(firstTermReg, secondTermReg))
        if (firstTerm == "false"):
            # Carrega número no registrador 1
            outputInstructions.append(self.device.LDI(firstTermReg, "1"))
            # Carrega número no registrador 2
            outputInstructions.append(
                self.device.LDI(secondTermReg, "0"))
            # Realiza a comparação
            outputInstructions.append(
                self.device.CP(firstTermReg, secondTermReg))
        if (firstTerm.isdigit() and secondTerm.isdigit()):
            # Carrega número no registrador 1
            outputInstructions.append(self.device.LDI(firstTermReg, firstTerm))
            # Carrega número no registrador 2
            outputInstructions.append(
                self.device.LDI(secondTermReg, secondTerm))
            # Realiza a comparação
            outputInstructions.append(
                self.device.CP(firstTermReg, secondTermReg))
        elif (firstTerm.isdigit() and not secondTerm.isdigit()):
            # Carrega número no registrador 1
            outputInstructions.append(self.device.LDI(firstTermReg, firstTerm))
            # Carrega da memória o valor da variável no registrador 2
            memAddress = self.varLog.getMem(secondTerm)
            outputInstructions.append(
                self.device.LDS(secondTermReg, memAddress))
            # Realiza a comparação
            outputInstructions.append(
                self.device.CP(firstTermReg, secondTermReg))
        elif (not firstTerm.isdigit() and secondTerm.isdigit()):
            # Carrega na memária o valor da variável no registrador 1
            memAddress = self.varLog.getMem(firstTerm)
            outputInstructions.append(
                self.device.LDS(firstTermReg, memAddress))
            # Carrega número no registrador 2
            outputInstructions.append(
                self.device.LDI(secondTermReg, secondTerm))
            # Realiza a comparação
            outputInstructions.append(
                self.device.CP(firstTermReg, secondTermReg))
        else:
            # Carrega na memária o valor da variável no registrador 1
            memAddress = self.varLog.getMem(firstTerm)
            outputInstructions.append(
                self.device.LDS(firstTermReg, memAddress))
            # Carrega na memária o valor da variável no registrador 2
            memAddress = self.varLog.getMem(secondTerm)
            outputInstructions.append(
                self.device.LDS(secondTermReg, memAddress))
            # Realiza a comparação
            outputInstructions.append(
                self.device.CP(firstTermReg, secondTermReg))
        self.device.removeRegister(firstTermReg)
        self.device.removeRegister(secondTermReg)
        return outputInstructions

    def getBranch(self, comparison, targetLabel):
        result = ""
        if comparison == "==":
            result = self.device.BREQ(targetLabel)
        elif comparison == "!=":
            result = self.device.BRNE(targetLabel)
        elif comparison == ">":
            result = self.device.BRSH(targetLabel)
        elif comparison == "<":
            result = self.device.BRLO(targetLabel)
        elif comparison == ">=":
            result = self.device.BRGE(targetLabel)
        elif comparison == "<=":
            result = self.device.BRLE(targetLabel)
        return result

    def getInvertedBranch(self, comparison, targetLabel):
        result = ""
        if comparison == "==":
            result = self.device.BRNE(targetLabel)
        elif comparison == "!=":
            result = self.device.BREQ(targetLabel)
        elif comparison == ">":
            result = self.device.BRLE(targetLabel)
        elif comparison == "<":
            result = self.device.BRGE(targetLabel)
        elif comparison == ">=":
            result = self.device.BRLO(targetLabel)
        elif comparison == "<=":
            result = self.device.BRSH(targetLabel)
        return result

    def getCondition(self, instructions, pos):
        # Funcao vai ler desde a abertura de "(" ate o fechamento de ")" se houver
        outputInstructions = []
        pos += 1
        if (instructions[pos].type != "FUNCTION ARGUMENT STARTER"):
            return outputInstructions, pos
        pos += 1
        instruction = instructions[pos]
        while (instruction.type != "FUNCTION ARGUMENT FINISHER"):
            outputInstructions.append(instruction)
            pos += 1
            instruction = instructions[pos]
        pos += 1
        return outputInstructions, pos

    def getScope(self, instructions, pos):
        # Funcao vai ler desde a abertura de "{" ate o fechamento de "}"
        outputInstructions = []
        if (instructions[pos].type == "CODE BLOCK STARTER"):
            pos += 1
        instruction = instructions[pos]
        scope = instruction.scope_depth
        # Se houver um outro bloco dentro, vai tudo junto
        while (instruction.type != "CODE BLOCK FINISHER" or instruction.scope_depth >= scope):
            outputInstructions.append(instruction)
            pos += 1
            instruction = instructions[pos]
        return outputInstructions, pos

    def pinConfigure(self, pin, configuration):
        outputCommand = []
        port, bit = self.device.getPinout(pin)
        port = "DDR" + port

        if (configuration == "0"):
            outputCommand.append(self.device.CBI(port,bit))
        elif (configuration == "1"):
            outputCommand.append(self.device.SBI(port,bit))

        return outputCommand

    def digitalPortWrite(self, pin, value):
        outputCommand = ""
        port, bit = self.device.getPinout(pin)
        port = "PORT" + port

        if (value == "0"):
            outputCommand = self.device.CBI(port, bit)
        else:
            outputCommand = self.device.SBI(port, bit)

        return outputCommand

    def digitalPortRead(self, pin, targetVar = None):
        outputCommands = []
        port, bit = self.device.getPinout(pin)
        readRegister = self.device.getRegister()
        port = "PIN" + port

        outputCommands.append(self.device.SBIS(port, bit))
        outputCommands.append(self.device.LDI(readRegister, "0"))
        outputCommands.append(self.device.SBIC(port, bit))
        outputCommands.append(self.device.LDI(readRegister, "1"))

        if (targetVar != None):
            memAddress = self.varLog.getMem(targetVar)
            outputCommands.append(self.device.STS(memAddress,readRegister))

        return outputCommands

    def getOperation(self, reg1, reg2, op):
        outputCommand = []
        if (op == "+"):
            outputCommand.append(self.device.ADD(reg1, reg2))
        elif (op == "-"):
            outputCommand.append(self.device.SUB(reg1, reg2))

        return outputCommand


    # == Funcoes Principais == #

    def arithmeticLogic(self, instructions, pos, labelName):
        targetVar = instructions[pos - 1].value
        targetAdd = self.varLog.getMem(targetVar)
        tokensAfter = []
        index = 1
        commands = []

        while (instructions[pos + index].type != "TERMINATOR"):
            tokensAfter.append(instructions[pos + index])
            index += 1

        receiverRegister = self.device.getRegister()
        auxRegister = self.device.getRegister()
        # x = y + 10 - 20 + b - 5;
        if (tokensAfter[0].value.isdigit()):
            commands.append(self.device.LDI(receiverRegister, tokensAfter[0].value))
        else:
            originMemAdd = self.varLog.getMem(tokensAfter[0].value)
            commands.append(self.device.LDS(receiverRegister, originMemAdd))

        index = 1
        while (index <= len(tokensAfter) - 2):
            if (tokensAfter[index+1].value.isdigit()):
                commands.append(self.device.LDI(auxRegister, tokensAfter[index+1].value))
            else:
                originMemAdd = self.varLog.getMem(tokensAfter[index+1].value)
                commands.append(self.device.LDS(auxRegister, originMemAdd))

            commands.extend(self.getOperation(receiverRegister, auxRegister, tokensAfter[index].value))
            index += 2

        commands.append(self.device.STS(targetAdd, receiverRegister))
        self.code.addInstructions(labelName, commands)

    def comparisonLogic(self):
        # >, <, ...
        pass

    def variableLogic(self, instructions, pos, labelName):
        targetVar = instructions[pos - 1].value
        targetAdd = self.varLog.getMem(targetVar)
        tokensAfter = []
        index = 1
        commands = []

        while (instructions[pos + index].type != "TERMINATOR"):
            tokensAfter.append(instructions[pos + index])
            index += 1

        if (len(tokensAfter) == 1):
            # x = const;
            if (tokensAfter[0].value.isdigit()):
                auxRegister = self.device.getRegister()
                commands.append(self.device.LDI(auxRegister, tokensAfter[0].value))
                commands.append(self.device.STS(targetAdd, auxRegister))
                auxRegister = self.device.removeRegister(auxRegister)
            # x = y;
            else:
                originMemAdd = self.varLog.getMem(tokensAfter[0].value)
                auxRegister = self.device.getRegister()
                commands.append(self.device.LDS(auxRegister, originMemAdd))
                commands.append(self.device.STS(targetAdd, auxRegister))
                auxRegister = self.device.removeRegister(auxRegister)
        else:
            # x = digitalRead pin;
            if (tokensAfter[0].type == "HARDWARE INTERACTION"):
                if (tokensAfter[0].value == "digitalRead"):
                    readPin = tokensAfter[1].value
                    outputCmds = self.digitalPortRead(readPin, targetVar)
                    commands.extend(outputCmds)
            # x = y + 5 - 2;
            else:
                self.arithmeticLogic(instructions, pos, labelName)

        self.code.addInstructions(labelName, commands)

    def keywordLogic(self, keyword, condition, instructions, currentLabelName,isEnd = True):
        code = []
        labelName = None
        # Realizar o código para a condicao
        if (keyword.value == "for"):
            pass
        elif (keyword.value == "while"):
            self.counter.addWhile()
            labelName = f"while_{self.counter.getWhile()}"
            self.code.addInstructions(currentLabelName, [self.device.RJMP(labelName)])
            self.code.addInstructions(currentLabelName, [f"endwhile_{self.counter.getWhile()}:"])
            self.code.addLabel(labelName)
            if (len(condition) == 1):
                loadConditionsCmd = self.loadConditions(condition[0].value)
                comparisonCmd = self.getBranch("==")
            else:
                loadConditionsCmd = self.loadConditions(condition[0].value, condition[2].value)
                comparisonCmd = self.getInvertedBranch(condition[1].value, f"endwhile_{self.counter.getWhile()}:")
            self.code.addInstructions(labelName, loadConditionsCmd)
            self.code.addInstructions(labelName, [comparisonCmd])
            self.translator(instructions, labelName)
            self.code.addInstructions(labelName, [self.device.RJMP(labelName)])
            self.counter.removeWhile()
        elif (keyword.value == "else"):
            labelName = f"else_{self.counter.getIf()}"
            self.code.addInstructions(
                currentLabelName, [self.device.RJMP(labelName)])
            self.code.addLabel(labelName)
            self.translator(instructions, labelName)
            self.code.addInstructions(
                labelName,
                [self.device.RJMP(f"endif_{self.counter.getIf()}")])
            self.code.addInstructions(currentLabelName, [f"endif_{self.counter.getIf()}:"])
            self.counter.resetElseif()
            self.counter.removeIf()
        else:
            if (keyword.value == "if"):
                self.counter.addIf()
                labelName = f"if_{self.counter.getIf()}"
                self.code.addLabel(labelName)
                self.translator(instructions, labelName)
                self.code.addInstructions(labelName,
                                          [self.device.RJMP(f"endif_{self.counter.getIf()}")])
            elif (keyword.value == "elseif"):
                self.counter.addElseif()
                labelName = f"elseif_{self.counter.getIf()}{self.counter.getElseif()}"
                self.code.addLabel(labelName)
                self.translator(instructions, labelName)
                self.code.addInstructions(labelName,
                                         [self.device.RJMP(f"endif_{self.counter.getIf()}")])
            if (isEnd):
                self.code.addInstructions(currentLabelName, [f"endif_{self.counter.getIf()}:"])
                self.counter.resetElseif()
                self.counter.removeIf()


            if (len(condition) == 1):
                loadConditionsCmd = self.loadConditions(condition[0].value)
                comparisonCmd = self.getBranch("==")
            else:
                loadConditionsCmd = self.loadConditions(condition[0].value, condition[2].value)
                comparisonCmd = self.getBranch(condition[1].value, labelName)
            self.code.addInstructions(currentLabelName, loadConditionsCmd)
            self.code.addInstructions(currentLabelName, [comparisonCmd])

    def translator(self, instructions, labelName = "main"):
        pos = 0
        while (pos < len(instructions)):
            # Separa cada instrucao
            pastInstruction = instructions[pos-1]
            currentInstruction = instructions[pos]
            nextInstruction = None
            if (pos < len(instructions) - 1):
                nextInstruction = instructions[pos+1]
            # == DATATYPE == #
            if (currentInstruction.type == "DATATYPE"):
                if (instructions[pos + 2].type == "TERMINATOR"):
                    self.varLog.add(nextInstruction.value)
                    pos += 2
            # == HARDWARE SETUP == #
            elif (currentInstruction.type == "HARDWARE SETUP"):
                hwLabelName = 'hwSetup'
                self.code.addLabel(hwLabelName)
                if (currentInstruction.value == "pinMode"):
                    pin = instructions[pos+1].value
                    configuration = instructions[pos+3].value
                    configCmd = self.pinConfigure(pin, configuration)
                    self.code.addInstructions(hwLabelName, configCmd)
                    pos += 3
            # == HARDWARE INTERACTION == #
            elif (currentInstruction.type == "HARDWARE INTERACTION"):
                if (currentInstruction.value == "digitalWrite"):
                    pin = instructions[pos+1].value
                    value = instructions[pos+3].value
                    writeCmd = self.digitalPortWrite(pin, value)
                    self.code.addInstructions(labelName, [writeCmd])
                    pos += 3
            # == OPERATORS == #
            elif (currentInstruction.type == "OPERATOR"):
                if (currentInstruction.value == "="):
                    self.variableLogic(instructions, pos, labelName)
            # == KEYWORD == #
            elif (currentInstruction.type == "KEYWORD"):
                # Isola as instrucoes dentro da condicao
                condition, pos = self.getCondition(instructions, pos)
                # Pega as instrucoes do escopo interno
                keywordInstructions, pos = self.getScope(instructions, pos)
                # Verifica se a condicional acaba ali caso seja IF/ELSE/ELSEIF
                isEnd = True
                if (pos + 1 < len(instructions) -1):
                    isEnd = instructions[pos + 1].value not in ['elseif', 'else']
                # Faz a condicao dos keywords
                self.keywordLogic(currentInstruction, condition,
                                  keywordInstructions, labelName, isEnd)
            # Vai para a proxima instrucao
            pos += 1

    # == Main == #

    def add(self, datatype):
        self.tokens.append(datatype)

    def run(self, device):
        self.device = device
        self.code.addLabel("main")
        self.translator(self.tokens, labelName="main")
        result = self.code.getCode()
        # == Debug Print == #
        # self.code.printDebug()
        # self.varLog.printLog()
        return result

class Counter:
    def __init__(self):
        self.ifDepth = 0
        self.ifLog = [0]
        self.elseifPos = -1
        self.ifOpenClose = []
        self.whileLog = [0]
        self.whileDepth = 0
        self.whileOpenClose = []

    def addWhile(self):
        if (self.whileDepth > len(self.whileLog) - 1):
            self.whileLog.append(0)
        self.whileLog[self.whileDepth] += 1
        self.whileDepth += 1
        self.whileOpenClose.clear()
        self.whileOpenClose.extend(self.whileLog)

    def removeWhile(self):
        print(self.whileOpenClose)
        print(self.whileDepth)
        self.whileOpenClose.pop()
        self.whileDepth -= 1

    def getWhile(self):
        return "_".join([str(i) for i in self.whileOpenClose])

    def addIf(self):
        if (self.ifDepth > len(self.ifLog) - 1):
            self.ifLog.append(0)
        self.ifLog[self.ifDepth] += 1
        self.ifDepth += 1
        self.ifOpenClose.clear()
        self.ifOpenClose.extend(self.ifLog)

    def addElseif(self):
        self.elseifPos += 1

    def resetElseif(self):
        self.elseifPos = 0

    def getElseif(self):
        alphabeth = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        return alphabeth[self.elseifPos]

    def removeIf(self):
        self.ifOpenClose.pop()
        self.ifDepth -= 1

    def getIf(self):
        return "_".join([str(i) for i in self.ifOpenClose])

    def printDebug(self):
        print(self.ifLog)