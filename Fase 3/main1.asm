start:
SBI DDRD, 3
main:
SBI PIND, 3
LDI R26, 200
STS $100, R26
CLR R26
LDS R18, $100
LDI R19, 0
while_1:
CP R18, R19
LDI R18, 199
STS $100, R18
CLR R18
BREQ next_1
RJMP while_1
next_1:
CBI PIND, 3
LDI R20, 200
STS $100, R20
CLR R20
LDS R29, $100
LDI R20, 0
while_2:
CP R29, R20
LDI R29, 199
STS $100, R29
CLR R29
BREQ next_2
RJMP while_2
next_2:
SBI PIND, 3
LDI R18, 200
STS $100, R18
CLR R18
LDS R28, $100
LDI R26, 0
while_3:
CP R28, R26
LDI R28, 199
STS $100, R28
CLR R28
BREQ next_3
RJMP while_3
next_3:
CBI PIND, 3
LDI R16, 200
STS $100, R16
CLR R16
LDS R27, $100
LDI R19, 0
while_4:
CP R27, R19
LDI R27, 199
STS $100, R27
CLR R27
BREQ next_4
RJMP while_4
next_4:
