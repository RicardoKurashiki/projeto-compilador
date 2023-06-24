#define __SFR_OFFSET 0
  
#include "avr/io.h"

.global start

start:
  sbi   DDRB,5
  
  ; x = 4
  ldi   r17,4
  sts   0x100, r17
  clr   r17
  
  ; y = 4 
  ldi   r18,4
  sts   0x104,r18
  clr   r18

  ; if (x == y)
  lds   r20,0x100
  lds   r21,0x104
  cp    r20,r21
  breq  if_1
  clr   r20
  clr   r21

  ; elseif (x > y)
  lds   r20,0x100
  lds   r21,0x104
  cp    r20,r21
  brsh  elseif_1a
  clr   r20
  clr   r21

  ; else
  rjmp else_1
endif_1:
  ; if (x < y)
  lds   r20,0x100
  lds   r21,0x104
  cp    r20,r21
  brlo  if_2
  clr   r20
  clr   r21

  rjmp  else_2
endif_2:
  ret

  ; if {}
if_1:
  ; if (y == 3)
  lds   r20,0x104
  ldi   r21,3
  cp    r20,21
  breq  if_1_1
  clr   r21
  clr   r20

  ; else
  rjmp  else_1_1
endif_1_1:
  ; z = 1
  ldi   r18,1
  sts   0x108,r18
  clr   r18
  ;sbi   PORTB, 5 ; Apenas ligando o led embutido para validar o funcionamento do if
  rjmp endif_1

  ; if {}
if_1_1:
  ; y = 6 
  ldi   r18,6
  sts   0x104,r18
  clr   r18
  sbi   PORTB, 5 ; Apenas ligando o led embutido para validar o funcionamento do if
  rjmp endif_1_1

  ; else {}
else_1_1:
  ; y = 1 
  ldi   r18,1
  sts   0x104,r18
  clr   r18
  cbi   PORTB, 5 ; Apenas ligando o led embutido para validar o funcionamento do if
  rjmp  endif_1_1

  ; elseif {}
elseif_1a:
  ; z = 2 
  ldi   r18,2
  sts   0x108,r18
  clr   r18
  cbi   PORTB, 5 ; Apenas desligando o led embutido para validar o funcionamento do if
  rjmp endif_1

  ; else {}
else_1:
  ; z = 3 
  ldi   r18,3
  sts   0x108,r18
  clr   r18
  cbi   PORTB, 5 ; Apenas desligando o led embutido para validar o funcionamento do if
  rjmp  endif_1

if_2:
  ; z = 3 
  ldi   r18,4
  sts   0x108,r18
  clr   r18
  rjmp  endif_2

else_2:
  rjmp  endif_2