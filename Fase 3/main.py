import tokens
from file import File
from arduino import Arduino

if __name__ == "__main__":
    device = Arduino()
    fileName = "script2"
    script = File(f"files/{fileName}.txt")          # Arquivo de Input
    output = File(f"{fileName}_output.asm")                  # Arquivo de Output
    print(f"== RODANDO CÓDIGO DE: {fileName} ==")
    interpreter = tokens.run(script)
    result = interpreter.run(device)
    print(result)
    output.writeFile(result)                   # Cria o arquivo main.asm
