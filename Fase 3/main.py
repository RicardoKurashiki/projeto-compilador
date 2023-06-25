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
    script = File(f"files/{fileName}.txt")              # Arquivo de Input
    output = File(f"output/{fileName}_output.asm")      # Arquivo de Output
    interpreter = tokens.run(script)
    result = interpreter.run(device)
    output.writeFile("")
    output.writeFile(result)
