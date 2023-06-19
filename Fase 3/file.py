class File:
    def __init__(self, path):
        self.path = path

    def getCode(self):
        with open(self.path, "r") as f:
            return f.read()

    def getLines(self):
        code = list()
        with open(self.path, 'r') as f:
            code = f.readlines()
        for i in range(0, len(code)):
            code[i] = code[i].replace('\n', '')
            code[i] = code[i].replace('\t', '')
        return code
    

    def writeFile(self, content):
        with open(self.path, 'w') as f:
            f.write(content)