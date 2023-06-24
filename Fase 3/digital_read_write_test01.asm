#define __SFR_OFFSET 0
  
#include "avr/io.h"

.global start

start:
  ; Led embutido como saída
  sbi   DDRB,5
  ; Porta digital PD2 (Pin 2) como entrada
  cbi   DDRD,2

while:
  ; while(true)
  ldi  r16,1
  ldi  r17,1
  cp   r16,r17
  brne endwhile
  
  ; lendo valor da porta digital e colocando no registrador 18
  sbis PIND,2
  ldi  r18,0
  sbic PIND,2
  ldi  r18,1

  ; if (pd2 == 1)
  ldi  r19,1
  cp   r18,r19
  breq lightUp
  ; else
  rjmp lightOff
endif:

  rjmp while

endwhile:
  ret

lightUp:
  sbi  PORTB,5
  rjmp endif

lightOff:
  cbi  PORTB,5
  rjmp endif
