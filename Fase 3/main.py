import tokens
from file import File
from arduino import Arduino

import sys

def getFileName():
    if (len(sys.argv) < 2):
        print("main.py <FILE_NAME>")
        exit(1)
    return sys.argv[1]

if __name__ == "__main__":
    print("== INICIO ==")
    fileName = getFileName()
    device = Arduino()
    print(f"Rodando arquivo: files/{fileName}.txt")
    script = File(f"files/{fileName}.txt")              # Arquivo de Input
    print(f"Salvando em: output/{fileName}_output.asm")
    output = File(f"output/{fileName}_output.asm")      # Arquivo de Output
    print()
    print("Separando instruções...")
    interpreter = tokens.run(script)
    print("Instruções separadas!")
    print("Traduzindo para asm...")
    result = interpreter.run(device)
    print("Tradução realizada!")
    output.writeFile("")
    print("Escrevendo no arquivo de output...")
    output.writeFile(result)
    print("Escrita feita!")
    print("== FIM ==")
