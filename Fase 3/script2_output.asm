#define __SFR_OFFSET 0
#include "avr/io.h"
.global hwSetup

hwSetup:
CBI DDRD, 2
SBI DDRD, 3

main:
LDI R30, 20
STS 0x100, R30
LDI R21, 10
LDI R29, 20
ADD R21, R29
STS 0x104, R21
RJMP while_1
endwhile_1:
CBI PORTD, 3
RET

while_1:
LDS R20, 0x100
LDS R17, 0x104
CP R20, R17
BRSH endwhile_1:
SBIS PIND, 2
LDI R16, 0
SBIC PIND, 2
LDI R16, 1
STS 0x108, R16
LDS R26, 0x108
LDI R27, 0
CP R26, R27
BREQ if_1
RJMP else_1
endif_1:
RJMP while_1

if_1:
SBI PORTD, 3
RJMP endif_1

else_1:
CBI PORTD, 3
RJMP endif_1
