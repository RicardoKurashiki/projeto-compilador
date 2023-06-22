from file import File
from data_type import DataType
# == Classes == #


class Interpreter:
    def __init__(self):
        self.actions = []

    def add(self, datatype):
        self.actions.append(datatype)


# == Variables == #


virgula = [',']
floatingPoint = ['.']
terminator = [';']
bool = ['true', 'false']
endpoints = ['break', 'return']
datatypes = ['int', 'float', 'void', 'boolean', 'byte']
keywords = ['for', 'while', 'do', 'if', 'elseif', 'else']
hardwareInteractions = [
    'pinMode', 'digitalRead', 'digitalWrite', 'analogRead', 'analogWrite',
    'serialBaud', 'serialAvailable', 'serialRead', 'serialWrite'
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
    global interpreter
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
                    interpreter.add(DataType("FLOAT", num, scope_depth))
                else:
                    interpreter.add(DataType("INT", num, scope_depth))
            # Caso seja um texto, faz diversas verificações
            elif char.isalpha():
                id = ""
                while char.isalpha() or char.isdigit():
                    id += char
                    char = seeNextPos(line, pos)
                    pos += 1
                # Se for um keyword, salva na lista como KEYWORD
                if id in keywords:
                    interpreter.add(DataType("KEYWORD", id, scope_depth))
                # Se for um boolean, salva na lista como BOOLEAN
                elif id in bool:
                    interpreter.add(DataType("BOOL", id, scope_depth))
                # Se for um endpoint, salva na lista como ENDPOINT
                elif id in endpoints:
                    interpreter.add(DataType("ENDPOINT", id, scope_depth))
                # Se for um datatype, salva na lista como DATATYPE
                elif id in datatypes:
                    interpreter.add(DataType("DATATYPE", id, scope_depth))
                # Se for um hardware interaction, salva na lista como HARDWARE INTERACTION
                elif id in hardwareInteractions:
                    interpreter.add(
                        DataType("HARDWARE INTERACTION", id, scope_depth))
                # Se não atender nenhum caso anterior, é um IDENTIFIER (variáveis e tal)
                else:
                    interpreter.add(DataType("IDENTIFIER", id, scope_depth))
            # Se for uma virgula, salva como VIRGULA
            elif char in virgula:
                interpreter.add(DataType("VIRGULA", char, scope_depth))
                pos += 1
            # Se for um ponto, salva na lista como FLOATING POINT
            elif char in floatingPoint:
                interpreter.add(DataType("FLOATING POINT", char, scope_depth))
                pos += 1
            # Se for um ponto e vírgula, salva na lista como TERMINATOR
            elif char in terminator:
                interpreter.add(DataType("TERMINATOR", char, scope_depth))
                pos += 1
            # Se for alguma estrutura
            elif char in codeBlockStarter:
                scope_depth += 1
                interpreter.add(
                    DataType("CODE BLOCK STARTER", char, scope_depth))
                pos += 1
            elif char in codeBlockFinisher:
                scope_depth -= 1
                interpreter.add(
                    DataType("CODE BLOCK FINISHER", char, scope_depth))
                pos += 1
            elif char in funcArgumentStarter:
                interpreter.add(
                    DataType("FUNCTION ARGUMENT STARTER", char, scope_depth))
                pos += 1
            elif char in funcArgumentFinisher:
                interpreter.add(
                    DataType("FUNCTION ARGUMENT FINISHER", char, scope_depth))
                pos += 1
            elif char in arrayStarter:
                interpreter.add(
                    DataType("ARRAY STARTER", char, scope_depth))
                pos += 1
            elif char in arrayFinisher:
                interpreter.add(
                    DataType("ARRAY FINISHER", char, scope_depth))
                pos += 1
            # Verifica operadores gerais
            elif char in comparisons:
                # Aqui é feita a verificação para operadores compostos (==, !=, >=, <=)
                if (char == ">" or char == "<" or char == "=" or char == "!"):
                    # Se a próxima posição for igual a =, é composto. Portanto add = ao char, e pula uma pos
                    if (seeNextPos(line, pos) == "="):
                        char += "="
                        pos += 1
                interpreter.add(DataType("COMPARISON", char, scope_depth))
                pos += 1
            elif char in operators:
                interpreter.add(
                    DataType("OPERATOR", char, scope_depth))
                pos += 1
            elif char in arithmetics:
                interpreter.add(
                    DataType("ARITHMETIC OPERATOR", char, scope_depth))
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
    for a in interpreter.actions:
        print(f"{a.type} | {a.value} | LVL. {a.scope_depth}")
