from arduino import Arduino
from variable_log import VariableLog

pinout = {
    "B": ["8", "9", "10", "11", "12", "13", "-", "-"],
    "C": ["A0", "A1", "A2", "A3", "A4", "A5", "-", "-"],
    "D": ["0", "1", "2", "3", "4", "5", "6", "7"]
}


class Interpreter:
    def __init__(self):
        self.tokens = []                # Tokens separados do txt
        self.device = Arduino()
        self.varLog = VariableLog()

    # == Funcoes Aux == #
    def loadConditions(self, firstTerm, secondTerm):
        outputInstructions = []
        firstTermReg = self.device.getRegister()
        secondTermReg = self.device.getRegister()
        if (firstTerm.isdigit() and secondTerm.isdigit()):
            # Carrega número no registrador 1
            outputInstructions.append(self.device.LDI(firstTermReg, firstTerm))
            # Carrega número no registrador 2
            outputInstructions.append(
                self.device.LDI(secondTermReg, secondTerm))
            # Realiza a comparação
            outputInstructions.append(
                self.device.CP(firstTermReg, secondTermReg))
            # Limpa registrador 1
            outputInstructions.append(self.device.CLR(firstTermReg))
            # Limpa registrador 2
            outputInstructions.append(self.device.CLR(secondTermReg))
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
            # Limpa registrador 1
            outputInstructions.append(self.device.CLR(firstTermReg))
            # Limpa registrador 2
            outputInstructions.append(self.device.CLR(secondTermReg))
        elif (not firstTerm.isdigit() and secondTerm.isdigit()):
            # Carrega na memária o valor da variável no registrador 1
            memAddress = self.varLog.getMem(firstTerm)
            outputInstructions.append(
                self.device.LDS(firstTerm, memAddress))
            # Carrega número no registrador 2
            outputInstructions.append(
                self.device.LDI(secondTermReg, secondTerm))
            # Realiza a comparação
            outputInstructions.append(
                self.device.CP(firstTermReg, secondTermReg))
            # Limpa registrador 1
            outputInstructions.append(self.device.CLR(firstTermReg))
            # Limpa registrador 2
            outputInstructions.append(self.device.CLR(secondTermReg))
        else:
            # Carrega na memária o valor da variável no registrador 1
            memAddress = self.varLog.getMem(firstTerm)
            outputInstructions.append(
                self.device.LDS(firstTerm, memAddress))
            # Carrega na memária o valor da variável no registrador 2
            memAddress = self.varLog.getMem(secondTerm)
            outputInstructions.append(
                self.device.LDS(secondTermReg, memAddress))
            # Realiza a comparação
            outputInstructions.append(
                self.device.CP(firstTermReg, secondTermReg))
            # Limpa registrador 1
            outputInstructions.append(self.device.CLR(firstTermReg))
            # Limpa registrador 2
            outputInstructions.append(self.device.CLR(secondTermReg))
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
        # Funcao vai ler desde a abertura de "(" ate o fechamento de ")"
        outputInstructions = []
        if (instructions[pos + 1].type == "FUNCTION ARGUMENT STARTER"):
            pos += 2
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
        pos += 1
        return outputInstructions, pos
    # == Funcoes Principais == #

    def arithmeticLogic(self):
        # +, -, /, *
        pass

    def comparisonLogic(self):
        # >, <, ...
        pass

    def variableLogic(self):
        pass

    def keywordLogic(self, keyword, condition, instructions):
        if (keyword.value == "if"):
            self.translator(instructions)
        elif (keyword.value == "elseif"):
            self.translator(instructions)
        elif (keyword.value == "else"):
            self.translator(instructions)
        elif (keyword.value == "while"):
            self.translator(instructions)
        return ""

    def hardwareLogic(self):
        pass

    def translator(self, instructions):
        # Retorna uma string que sera o codigo
        code = ""
        pos = 0
        print(" ".join([i.value for i in instructions]))
        while (pos < len(instructions)):
            # Separa cada instrucao
            pastInstruction = instructions[pos-1]
            currentInstruction = instructions[pos]
            nextInstruction = None
            if (pos < len(instructions) - 1):
                nextInstruction = instructions[pos+1]
            # Compara tipo de instrucao
            if (currentInstruction.type == "KEYWORD"):
                condition, pos = self.getCondition(instructions, pos)
                keywordInstructions, pos = self.getScope(instructions, pos)
                self.keywordLogic(currentInstruction,
                                  condition, keywordInstructions)
            # Vai para a proxima instrucao
            pos += 1
        return code

    # == Main == #

    def add(self, datatype):
        self.tokens.append(datatype)

    def run(self, device):
        self.device = device
        code = self.translator(self.tokens)
        # self.varLog.printLog()
        return code
