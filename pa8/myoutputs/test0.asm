; Symbol table 
; name cur type Type.INT location 0x20000000
; name test type Type.STRING location 0x10000000 value "Hello World\n"

.section .text
;Current temp: 
;IR Code: 
LA t0, 0x10000000
PUTS t0
LI t1, 7
PUTI t1
LI t2, 0
HALT

.section .strings
0x10000000 "Hello World\n"
