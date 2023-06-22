class File:
    def __init__(self, path):
        self.path = path

    def getCode(self):
        with open(self.path, "r") as f:
            return f.read().replace("\n", " ")

    def getLines(self):
        code = self.getCode()
        code = code.split(" ")
        return [c for c in code if c != ""]

    def writeFile(self, content):
        with open(self.path, 'w') as f:
            f.write(content)
