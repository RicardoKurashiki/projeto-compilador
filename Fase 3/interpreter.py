from file import File

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
comparisons = ['>', '<', '>=', '<=','==', '!=']
operators = ['=', '!', '&&', '||', '&', '|']
arithmetics = ['+', '-', '*', '/']

# == Private == #
def _findTokens(c):
    # Ve qual é o char da posição após a atual
    def seeNextPos(code, pos):
        if pos + 1 >= len(code):
                return ''
        return code[pos + 1]
    
    def scanLine(line):
        pos = 0
        while pos < len(line):
            char = line[pos]
            # Verifica se é um número, e se for, apenas pega o valor e salva como NUM
            if (char.isdigit()): 
                num = ""
                while char.isdigit():
                    num += char
                    char = seeNextPos(line, pos)
                    pos+=1
                    tokens.append(("NUM", num))
            # Caso seja um texto, faz diversas verificações
            elif char.isalpha():
                id = ""
                while char.isalpha() or char.isdigit():
                    id += char
                    char = seeNextPos(line, pos)
                    pos+=1
                # Se for um keyword, salva na lista como KEYWORD
                if id in keywords:
                    tokens.append(("KEYWORD", id))
                # Se for um boolean, salva na lista como BOOLEAN
                elif id in bool:
                    tokens.append(("BOOLEAN", id))
                # Se for um endpoint, salva na lista como ENDPOINT
                elif id in endpoints:
                    tokens.append(("ENDPOINT", id))
                # Se for um datatype, salva na lista como DATATYPE
                elif id in datatypes:
                    tokens.append(("DATATYPE", id))
                # Se for um hardware interaction, salva na lista como HARDWARE INTERACTION
                elif id in hardwareInteractions:
                    tokens.append(("HARDWARE INTERACTION", id))
                # Se não atender nenhum caso anterior, é um IDENTIFIER (variáveis e tal)
                else:
                    tokens.append(("IDENTIFIER", id))
            # Verifica se é um operador
            elif char in operator:
                # Aqui é feita a verificação para operadores compostos (==, !=, >=, <=)
                if (char == ">" or char == "<" or char == "=" or char == "!"):
                    # Se a próxima posição for igual a =, é composto. Portanto add = ao char, e pula uma pos
                    if (seeNextPos(line, pos) == "="):
                        char += "="
                        pos += 1
                tokens.append(("OPERATOR", char))
                pos += 1
            # Se for uma virgula, salva como VIRGULA
            elif char in virgula:
                tokens.append(("VIRGULA", char))
                pos += 1
            # Se for um ponto, salva na lista como FLOATING POINT
            elif char in floatingPoint:
                tokens.append(("FLOATING POINT", char))
                pos += 1
            # Se for um ponto e vírgula, salva na lista como TERMINATOR
            elif char in terminator:
                tokens.append(("TERMINATOR", char))
                pos += 1
            else:
                break

    tokens = [] # Tokens que serão encontrados
    code = c.split() # Cada linha do código
    # Lê cada linha do código inteiro
    for line in code:
        scanLine(line) # Realiza a verificação de cada char

    return tokens

# == Public == #
def run(f):
    code = f.getCode()
    tokens = _findTokens(code)
    print(tokens)