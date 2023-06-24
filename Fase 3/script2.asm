#define __SFR_OFFSET 0
  
#include "avr/io.h"

.global start

start:
  cbi DDRD,2
  ; Única alteração present no código original, aqui estou trabalhando com o led embutido
  sbi DDRB,5

  ldi r16,34
  sts 0x200,r16

  ldi r17,34
  sts 0x204,r17

  rjmp while_1
endwhile_1:
  ret

while_1:
  ; while (x >= y)
  lds r16,0x200
  lds r17,0x204
  cp  r16,r17
  brlo endwhile_1

  ; digitalRead 2
  sbis PIND,2
  ldi r18,0
  sbic PIND,2
  ldi r18,1

  ; buttonStatus = digitalRead 2
  sts 0x208,r18

  ; if (buttonStatus == 0)
  ldi r17,0
  lds r19,0x208
  cp  r17,r19
  breq if_1

  ; else
  rjmp else_1
endif_1:
  rjmp while_1

if_1:
  ; digitalWrite 3,1
  sbi  PORTB,5
  rjmp endif_1

else_1:
  ; digitalWrite 3,0
  cbi  PORTB,5
  rjmp endif_1