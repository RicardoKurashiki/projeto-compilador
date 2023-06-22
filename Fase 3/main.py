import interpreter
from file import File

if __name__ == "__main__":
    script = File("script2.txt")         # Arquivo de Input
    output = File("main.asm")           # Arquivo de Output
    result = interpreter.run(script)    # Retorna uma String com o código
    # output.writeFile(result)            # Cria o arquivo main.asm
