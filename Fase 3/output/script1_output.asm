#define __SFR_OFFSET 0
#include "avr/io.h"
.global hwSetup

hwSetup:
SBI DDRB, 5

main:
SBI PORTB, 5
LDI R20, 200
STS 0x400, R20
JMP while_1
endwhile_1:
CBI PORTB, 5
LDI R28, 200
STS 0x400, R28
JMP while_2
endwhile_2:
SBI PORTB, 5
LDI R19, 200
STS 0x400, R19
JMP while_3
endwhile_3:
CBI PORTB, 5
LDI R28, 200
STS 0x400, R28
JMP while_4
endwhile_4:
RET

while_1:
LDS R23, 0x400
LDI R25, 0
CP R23, R25
BREQ endwhile_1
LDS R25, 0x400
LDI R28, 1
SUB R25, R28
STS 0x400, R25
JMP while_1

while_2:
LDS R24, 0x400
LDI R28, 0
CP R24, R28
BREQ endwhile_2
LDS R25, 0x400
LDI R21, 1
SUB R25, R21
STS 0x400, R25
JMP while_2

while_3:
LDS R21, 0x400
LDI R27, 0
CP R21, R27
BREQ endwhile_3
LDS R19, 0x400
LDI R26, 1
SUB R19, R26
STS 0x400, R19
JMP while_3

while_4:
LDS R24, 0x400
LDI R16, 0
CP R24, R16
BREQ endwhile_4
LDS R20, 0x400
LDI R23, 1
SUB R20, R23
STS 0x400, R20
JMP while_4
