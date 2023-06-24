class Code:
    def __init__(self):
        self.code = {}

    def addLabel(self, labelName):
        if (labelName not in list(self.code.keys())):
            self.code[labelName] = []

    def addInstructions(self, labelName, instructions):
        self.code[labelName].extend(instructions)

    def getCode(self):
        code = ""
        setupLabel = "hwSetup"
        # Init
        code += "#define __SFR_OFFSET 0\n"
        code += "#include \"avr/io.h\"\n"
        code += f".global {setupLabel}\n\n"
        code += f"{setupLabel}:\n"

        if (setupLabel in list(self.code.keys())):
            code += "\n".join(self.code[setupLabel])
            code += "\n"
            del self.code[setupLabel]
        
        labels = list(self.code.keys())

        for label in labels:
            code += f"{label}:\n"
            code += "\n".join(self.code[label])
            code += "\n"
        return code

    def printDebug(self):
        print(self.code)