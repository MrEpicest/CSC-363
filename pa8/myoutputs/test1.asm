; Symbol table 
; name cur type Type.INT location 0x20000000

.section .text
;Current temp: 
;IR Code: 
LI t0, 0
LA t1, 0x20000000
SW t0, 0(t1)
LA t3, 0x20000000
LW t4, 0(t3)
LI t2, 4
ADD t5, t4, t2
LA t6, 0x20000000
SW t5, 0(t6)
LA t7, 0x20000000
LW t8, 0(t7)
PUTI t8
LI t9, 0
HALT

.section .strings
