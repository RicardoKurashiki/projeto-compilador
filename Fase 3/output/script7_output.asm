#define __SFR_OFFSET 0
#include "avr/io.h"
.global hwSetup

hwSetup:
SBI DDRB, 5

main:
LDI R30, 255
STS 0x400, R30
LDS R17, 0x400
LDI R20, 1
AND R17, R20
STS 0x400, R17
LDS R23, 0x400
LDI R17, 1
CP R23, R17
BREQ if_1
JMP else_1
endif_1:
RET

if_1:
CBI PORTB, 5
JMP endif_1

else_1:
SBI PORTB, 5
JMP endif_1
