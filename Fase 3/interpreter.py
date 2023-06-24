from arduino import Arduino
from variable_log import VariableLog


class Interpreter:
    def __init__(self):
        self.tokens = []                # Tokens separados do txt
        self.device = Arduino()
        self.varLog = VariableLog()
        self.counter = Counter()

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

    # == Funcoes Principais == #

    def arithmeticLogic(self):
        # +, -, /, *
        pass

    def comparisonLogic(self):
        # >, <, ...
        pass

    def variableLogic(self):
        pass

    def keywordLogic(self, keyword, condition, instructions, isEnd=True):
        code = []
        self.counter.printDebug()
        if (keyword.value == "if"):
            self.counter.addIf()
            code.append(f"if_stat{self.counter.getIf()}:")
            result = self.translator(instructions)
            code.append(self.device.RJMP(f"end_if{self.counter.getIf()}"))
        elif (keyword.value == "elseif"):
            code.append(f"elseif_stat{self.counter.getIf()}:")
            result = self.translator(instructions)
            code.append(self.device.RJMP(f"end_if{self.counter.getIf()}"))
        elif (keyword.value == "else"):
            code.append(f"else_stat{self.counter.getIf()}:")
            result = self.translator(instructions)
            code.append(self.device.RJMP(f"end_if{self.counter.getIf()}"))
        elif (keyword.value == "while"):
            self.counter.addWhile()
            result = self.translator(instructions)
            code.append(self.device.RJMP(f"end_while{self.counter.getWhile()}"))
        self.counter.printDebug()
        code.extend(result)
        if (keyword.value in ["if", "elseif", "else"] and isEnd):
            code.append(f"end_if{self.counter.popIf()}:")
        elif (keyword.value == "while"):
            code.append(f"end_while{self.counter.popWhile()}:")
        return code

    def hardwareLogic(self):
        pass

    def translator(self, instructions):
        # Retorna uma string que sera o codigo
        code = []
        pos = 0
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
                isEnd = instructions[pos+1].value not in ['elseif', 'else']
                result = self.keywordLogic(currentInstruction,
                                  condition, keywordInstructions, isEnd)
                code.extend(result)
            # Vai para a proxima instrucao
            pos += 1
        return code

    # == Main == #

    def add(self, datatype):
        self.tokens.append(datatype)

    def run(self, device):
        self.device = device
        code = self.translator(self.tokens)
        for _ in range(0, 50):
            print()
        for c in code:
            print(c)
            if ("end" not in c):
                print("...")
        print("...")
        for _ in range(0, 50):
            print()
        # self.varLog.printLog()
        return code

class Counter:
    def __init__(self):
        # Eh necessario ser stack para conseguir ter varios aninhados
        self.if_counter = 0
        self.while_counter = 0
        self.if_total = 0
        self.while_total = 0
        self.if_stack = []
        self.while_stack = []

    def addIf(self):
        self.if_total += 1
        self.if_counter = self.if_total
        self.if_stack.append(self.if_counter)

    def addWhile(self):
        self.while_total += 1
        self.while_counter = self.while_total
        self.while_stack.append(self.while_counter)

    def getIf(self):
        return self.if_counter

    def getWhile(self):
        return self.while_counter

    def popIf(self):
        value = self.if_stack.pop()
        self.if_counter = value - 1
        return value

    def popWhile(self):
        value = self.while_stack.pop()
        self.while_counter = value - 1
        return value

    def printDebug(self):
        print("\n== DEBUG START ==")
        print(f"IF STACK: {self.if_stack}")
        print(f"WHILE STACK: {self.while_stack}")
        print(f"IF COUNTER: {self.if_counter}")
        print(f"WHILE COUNTER: {self.while_counter}")
        print(f"IF TOTAL: {self.if_total}")
        print(f"WHILE TOTAL: {self.while_total}")
        print("== DEBUG END ==\n")