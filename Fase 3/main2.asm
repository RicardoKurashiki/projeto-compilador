start:
CBI DDRD, 2
SBI DDRD, 3
main:
LDI R26, 20
STS $100, R26
CLR R26
LDI R20, 34
STS $104, R20
CLR R20
LDS R27, $100
LDS R17, $104
while_1:
CP R17, R23
LDI R19, 3
STS $110, R19
CLR R19
SBI PIND, 3
BRLO next_1
RJMP while_1
next_1:
CBI PIND, 3
BRLO next_1
RJMP while_1
next_1:
BRLO next_1
RJMP while_1
next_1:
