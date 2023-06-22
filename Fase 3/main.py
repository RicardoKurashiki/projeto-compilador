import tokens
from file import File
from arduino import Arduino

if __name__ == "__main__":
    device = Arduino()
    fileType = 3
    script = File(f"files/script{fileType}.txt")          # Arquivo de Input
    output = File(f"main{fileType}.asm")                   # Arquivo de Output
    interpreter = tokens.run(script)
    result = interpreter.getCode(device)
    print(result)
    output.writeFile(result)                   # Cria o arquivo main.asm
