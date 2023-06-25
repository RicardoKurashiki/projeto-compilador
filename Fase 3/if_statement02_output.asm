#define __SFR_OFFSET 0
#include "avr/io.h"
.global hwSetup

hwSetup:
SBI DDRB, 5

main:
LDI R23, 45
STS 0x100, R23
LDS R17, 0x100
LDI R16, 10
CP R17, R16
BRSH if_1
RJMP else_1
endif_1:
RET

if_1:
LDS R21, 0x100
LDI R29, 40
CP R21, R29
BRSH if_1_1
LDS R16, 0x100
LDI R26, 30
CP R16, R26
BRSH elseif_1_1a
LDS R24, 0x100
LDI R23, 20
CP R24, R23
BRSH elseif_1_1b
RJMP else_1_1
endif_1_1:
RJMP endif_1

if_1_1:
SBI PORTB, 5
RJMP endif_1_1

elseif_1_1a:
CBI PORTB, 5
RJMP endif_1_1

elseif_1_1b:
CBI PORTB, 5
RJMP endif_1_1

else_1_1:
CBI PORTB, 5
RJMP endif_1_1

else_1:
CBI PORTB, 5
RJMP endif_1
