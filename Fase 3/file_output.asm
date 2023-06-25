#define __SFR_OFFSET 0
#include "avr/io.h"
.global hwSetup

hwSetup:
CBI DDRD, 2
SBI DDRB, 5

main:
RJMP while_1
endwhile_1:
CBI PORTB, 5
RET

while_1:
LDI R25, 1
LDI R28, 1
CP R25, R28
BRNE endwhile_1
SBIS PIND, 2
LDI R23, 0
SBIC PIND, 2
LDI R23, 1
STS 0x200, R23
LDS R24, 0x200
LDI R26, 0
CP R24, R26
BREQ if_1
RJMP else_1
endif_1:
RJMP while_1

if_1:
SBI PORTB, 5
RJMP endif_1

else_1:
CBI PORTB, 5
RJMP endif_1
