#define __SFR_OFFSET 0
  
#include "avr/io.h"

.global start

start:
  sbi   DDRB,5
  
  ldi   r17,3
  sts   0x100, r17
  clr   r17
  
  ldi   r18,5
  sts   0x104,r18
  clr   r18

  lds   r20,0x100
  lds   r21,0x104
  cp    r20,r21
  breq if_stat1
  clr   r20
  clr   r21

  lds   r20,0x100
  lds   r21,0x104
  cp    r20,r21
  brsh elseif_stat1
  clr   r20
  clr   r21

  rjmp else_stat1

if_stat1:
  sbi   PORTB, 5
  rjmp endif1

elseif_stat1:
  cbi   PORTB, 5
  rjmp endif1

else_stat1:
  cbi   PORTB, 5

endif1:
  ret
