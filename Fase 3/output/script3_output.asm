#define __SFR_OFFSET 0
#include "avr/io.h"
.global hwSetup

hwSetup:
CBI DDRD, 2
SBI DDRB, 5

main:
JMP while_1
endwhile_1:
CBI PORTB, 5
RET

while_1:
LDI R19, 1
LDI R21, 1
CP R19, R21
BRNE endwhile_1
SBIS PIND, 2
LDI R22, 0
SBIC PIND, 2
LDI R22, 1
STS 0x400, R22
LDS R20, 0x400
LDI R23, 0
CP R20, R23
BREQ if_1
JMP else_1
endif_1:
JMP while_1

if_1:
SBI PORTB, 5
JMP endif_1

else_1:
CBI PORTB, 5
JMP endif_1
