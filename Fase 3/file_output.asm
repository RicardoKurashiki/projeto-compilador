#define __SFR_OFFSET 0
#include "avr/io.h"
.global hwSetup

hwSetup:
SBI DDRB, 5

main:
LDI R23, 255
STS 0x200, R23
LDS R24, 0x200
LDI R28, 1
AND R24, R28
STS 0x200, R24
LDS R29, 0x200
LDI R18, 1
CP R29, R18
BREQ if_1
RJMP else_1
endif_1:
RET

if_1:
CBI PORTB, 5
RJMP endif_1

else_1:
SBI PORTB, 5
RJMP endif_1
