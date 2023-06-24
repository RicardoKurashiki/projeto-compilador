import tokens
from file import File
from arduino import Arduino

if __name__ == "__main__":
    device = Arduino()
    fileName = "basic_operation"
    script = File(f"files/{fileName}.txt")          # Arquivo de Input
    output = File(f"{fileName}_output.asm")                  # Arquivo de Output
    interpreter = tokens.run(script)
    result = interpreter.run(device)
    print(result)
    output.writeFile(result)                   # Cria o arquivo main.asm
