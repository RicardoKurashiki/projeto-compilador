import tokens
from file import File
from arduino import Arduino

if __name__ == "__main__":
    device = Arduino()
    script = File("files/script2.txt")          # Arquivo de Input
    output = File("main.asm")                   # Arquivo de Output
    interpreter = tokens.run(script)
    print(interpreter.getCode(device))
    # output.writeFile(result)                   # Cria o arquivo main.asm
