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
    fileName = getFileName()
    device = Arduino()
    script = File(f"files/{fileName}.txt")          # Arquivo de Input
    output = File(f"file_output.asm")                  # Arquivo de Output
    print(f"== RODANDO CÓDIGO DE: {fileName} ==")
    interpreter = tokens.run(script)
    result = interpreter.run(device)
    print(result)
    output.writeFile(result)                   # Cria o arquivo main.asm
