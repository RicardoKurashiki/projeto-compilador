import random as rd


class Arduino:
    def __init__(self):
        self.max_mem = 65535
        self.mem = 512
        self.registers = {
            'R16': True,
            'R17': True,
            'R18': True,
            'R19': True,
            'R20': True,
            'R21': True,
            'R22': True,
            'R23': True,
            'R24': True,
            'R25': True,
            'R26': True,
            'R27': True,
            'R28': True,
            'R29': True,
            'R30': True,
            'R31': True
        }

    def getRegister(self):
        return rd.choice([r for r in self.registers if self.registers[r] == True])

    def setRegister(self, reg):
        if (self.registers[reg]):
            self.registers[reg] = False

    def removeRegister(self, reg):
        if (not self.registers[reg]):
            self.registers[reg] = True

    # Instructions - Arithmetical and logical operations
    def ADD(self, rx, ry):
        return f"ADD {rx}, {ry}"

    def AND(self, rx, ry):
        return f"AND {rx}, {ry}"

    def OR(self, rx, ry):
        return f"OR {rx}, {ry}"

    def EOR(self, rx, ry):
        return f"EOR {rx}, {ry}"

    def SUB(self, rx, ry):
        return f"SUB {rx}, {ry}"

    def CP(self, rx, ry):
        return f"CP {rx}, {ry}"

    def CPI(self, rh, k):
        return f"CPI {rh}, {k}"

    def INC(self, rx):
        return f"INC {rx}"

    def DEC(self, rx):
        return f"DEC {rx}"

    def CLR(self, rx):
        return f"CLR {rx}"

    # Instructions - Jump instructions
    def RJMP(self, k):
        return f"RJMP {k}"

    def RET(self):
        return "RET"

    def BREQ(self, k):  # Skip (==)
        return f"BREQ {k}"

    def BRNE(self, k):  # Skip (!=)
        return f"BRNE {k}"

    def BRSH(self, k):  # Skip (>)
        return f"BRSH {k}"

    def BRGE(self, k):  # Skip (>=)
        return f"BRGE {k}"

    def BRLO(self, k):  # Skip (<)
        return f"BRLO {k}"

    def BRLE(self, k):  # Skip (<=)
        return f"BRLE {k}"

    # Instructions - Data copy and load instructions
    def MOV(self, rx, ry):
        return f"MOV {rx}, {ry}"

    def LDI(self, rh, k):
        return f"LDI {rh}, {k}"

    def LDS(self, rh, a):
        return f"LDS {rh}, ${a}"

    def STS(self, a, rh):
        return f"STS ${a}, {rh}"

    # Instructions - Controller instructions

    def NOP(self):
        return "NOP"
