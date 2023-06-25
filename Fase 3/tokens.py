from file import File
from instruction import Instruction
from interpreter import Interpreter

# == Variables == #


virgula = [',']
floatingPoint = ['.']
terminator = [';']
bool = ['true', 'false']
endpoints = ['break', 'return']
datatypes = ['int', 'float', 'void', 'boolean', 'byte']
keywords = ['for', 'while', 'do', 'if', 'elseif', 'else']

hardwareSetup = ['pinMode', 'serialBaud']
hardwareInteractions = [
    'digitalRead', 'digitalWrite', 'analogRead', 'analogWrite',
    'serialAvailable', 'serialRead', 'serialWrite'
]

codeBlockStarter = ["{"]
codeBlockFinisher = ["}"]
funcArgumentStarter = ["("]
funcArgumentFinisher = [")"]
arrayStarter = ["["]
arrayFinisher = ["]"]
comparisons = ['>', '<', '>=', '<=', '==', '!=']
operators = ['=', '!', '&&', '||', '&', '|']
arithmetics = ['+', '-', '*', '/']

interpreter = Interpreter()

# == Private == #


def _findTokens(c):
    global scope_depth
    # Ve qual é o char da posição após a atual
    scope_depth = -1

    def seeNextPos(code, pos):
        if pos + 1 >= len(code):
            return ''
        return code[pos + 1]

    def scanLine(line):
        global scope_depth
        pos = 0
        while pos < len(line):
            char = line[pos]
            # Verifica se é um número, e se for, apenas pega o valor e salva como NUM
            if (char.isdigit()):
                num = ""
                while char.isdigit():
                    num += char
                    char = seeNextPos(line, pos)
                    pos += 1
                if ("." in num):
                    interpreter.add(Instruction("FLOAT", num, scope_depth))
                else:
                    interpreter.add(Instruction("INT", num, scope_depth))
            # Caso seja um texto, faz diversas verificações
            elif char.isalpha():
                id = ""
                while char.isalpha() or char.isdigit():
                    id += char
                    char = seeNextPos(line, pos)
                    pos += 1
                # Se for um keyword, salva na lista como KEYWORD
                if id in keywords:
                    interpreter.add(Instruction("KEYWORD", id, scope_depth))
                # Se for um boolean, salva na lista como BOOLEAN
                elif id in bool:
                    interpreter.add(Instruction("BOOL", id, scope_depth))
                # Se for um endpoint, salva na lista como ENDPOINT
                elif id in endpoints:
                    interpreter.add(Instruction("ENDPOINT", id, scope_depth))
                # Se for um Instruction, salva na lista como Instruction
                elif id in datatypes:
                    interpreter.add(Instruction(
                        "DATATYPE", id, scope_depth))
                # Se for um hardware interaction, salva na lista como HARDWARE INTERACTION
                elif id in hardwareSetup:
                    interpreter.add(
                        Instruction("HARDWARE SETUP", id, scope_depth))
                elif id in hardwareInteractions:
                    interpreter.add(
                        Instruction("HARDWARE INTERACTION", id, scope_depth))
                # Se não atender nenhum caso anterior, é um IDENTIFIER (variáveis)
                else:
                    interpreter.add(Instruction("IDENTIFIER", id, scope_depth))
            # Se for uma virgula, salva como VIRGULA
            elif char in virgula:
                interpreter.add(Instruction("VIRGULA", char, scope_depth))
                pos += 1
            # Se for um ponto, salva na lista como FLOATING POINT
            elif char in floatingPoint:
                interpreter.add(Instruction(
                    "FLOATING POINT", char, scope_depth))
                pos += 1
            # Se for um ponto e vírgula, salva na lista como TERMINATOR
            elif char in terminator:
                interpreter.add(Instruction("TERMINATOR", char, scope_depth))
                pos += 1
            # Se for alguma estrutura
            elif char in codeBlockStarter:
                scope_depth += 1
                interpreter.add(
                    Instruction("CODE BLOCK STARTER", char, scope_depth))
                pos += 1
            elif char in codeBlockFinisher:
                scope_depth -= 1
                interpreter.add(
                    Instruction("CODE BLOCK FINISHER", char, scope_depth))
                pos += 1
            elif char in funcArgumentStarter:
                interpreter.add(
                    Instruction("FUNCTION ARGUMENT STARTER", char, scope_depth))
                pos += 1
            elif char in funcArgumentFinisher:
                interpreter.add(
                    Instruction("FUNCTION ARGUMENT FINISHER", char, scope_depth))
                pos += 1
            elif char in arrayStarter:
                interpreter.add(
                    Instruction("ARRAY STARTER", char, scope_depth))
                pos += 1
            elif char in arrayFinisher:
                interpreter.add(
                    Instruction("ARRAY FINISHER", char, scope_depth))
                pos += 1
            # Verifica operadores gerais
            elif char in comparisons:
                # Aqui é feita a verificação para operadores compostos (==, !=, >=, <=)
                if (char == ">" or char == "<" or char == "=" or char == "!"):
                    # Se a próxima posição for igual a =, é composto. Portanto, add = ao char, e pula uma pos
                    if (seeNextPos(line, pos) == "="):
                        char += "="
                        pos += 1
                interpreter.add(Instruction("COMPARISON", char, scope_depth))
                pos += 1
            elif char in operators:
                if (char == "=" or char == "!"):
                    if (seeNextPos(line, pos) == "="):
                        char += "="
                        pos += 1
                        interpreter.add(
                            Instruction("COMPARISON", char, scope_depth))
                    else:
                        interpreter.add(
                            Instruction("OPERATOR", char, scope_depth))
                else:
                    interpreter.add(
                        Instruction("OPERATOR", char, scope_depth))
                pos += 1
            elif char in arithmetics:
                interpreter.add(
                    Instruction("ARITHMETIC OPERATOR", char, scope_depth))
                pos += 1
            else:
                break

    # Lê cada linha do código inteiro
    for line in c:
        scanLine(line)  # Realiza a verificação de cada char

# == Public == #


def run(f):
    code = f.getLines()
    _findTokens(code)
    return interpreter
