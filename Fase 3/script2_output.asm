#define __SFR_OFFSET 0
#include "avr/io.h"
.global hwSetup

hwSetup:
CBI DDRD, 2
SBI DDRB, 5

main:
LDI R20, 20
STS 0x200, R20
LDI R22, 20
STS 0x204, R22
RJMP while_1
endwhile_1:
CBI PORTB, 5
RET

while_1:
LDS R24, 0x200
LDS R29, 0x204
CP R24, R29
BRNE endwhile_1
SBIS PIND, 2
LDI R19, 0
SBIC PIND, 2
LDI R19, 1
STS 0x208, R19
LDS R31, 0x208
LDI R25, 0
CP R31, R25
BREQ if_1
RJMP else_1
endif_1:
RJMP while_1

if_1:
CBI PORTB, 5
RJMP endif_1

else_1:
SBI PORTB, 5
RJMP endif_1
