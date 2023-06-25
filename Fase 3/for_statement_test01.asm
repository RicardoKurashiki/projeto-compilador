#define __SFR_OFFSET 0
#include "avr/io.h"
.global hwSetup

hwSetup:
main:
  ; x = 0
  ldi r16,10
  sts 0x200,r16

  ; for (i = 0;...)
  ldi r17,0
  sts 0x204,r17
  rjmp for_1
endfor_1:
  RET

for_1:
  ; for (...; i < 10; ...)
  lds r18,0x204
  ldi r19,10
  brge endfor_1

  ; for(...;...; i = i + 1)
  lds r18,0x204
  ldi r19,1
  sum r18,r19
  sts 0x204,r18

  ; x = x + 2;
  lds r20,0x200
  ldi r21,2
  sum r20,r21
  sts 0x200,r20

  rjmp endfor_1
