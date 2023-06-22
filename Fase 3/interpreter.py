from arduino import Arduino


class Interpreter:
    def __init__(self):
        self.tokens = []
        self.startOperations = []
        self.mainOperations = []
        self.device = Arduino()

    # def _separateOperations(self):
    #     for t in self.tokens:
    #         if (t.type in startOp):
    #             self.startOperations.append(t)
    #         # FAZER LÓGICA DE FUNCAO
    #         else:
    #             self.mainOperations.append(t)

    def _translate(self):
        def setNewMemorySpace(type):
            if (type == "INT"):

                pass

        for index in range(0, len(self.tokens)):
            token = self.tokens[index]
            if (token.type == "INT"):
                pass

    def add(self, datatype):
        self.tokens.append(datatype)

    def getCode(self, device):
        self.device = device
        self._translate()
        return ""
