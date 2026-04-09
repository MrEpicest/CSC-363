; Symbol table 
; name cur type Type.INT location 0x20000000

.section .text
;Current temp: 
;IR Code: 
LI t1, 0
LA t2, 0x20000000
SW t1, 0(t2)
loop1:
LA t4, 0x20000000
LW t5, 0(t4)
LI t3, 10
; Left type: Type.INT
; Right type: Type.INT
BGE t5, t3, else0
LA t7, 0x20000000
LW t8, 0(t7)
LI t6, 4
ADD t9, t8, t6
LA t10, 0x20000000
SW t9, 0(t10)
J loop1
else1:
done1:
LA t11, 0x20000000
LW t12, 0(t11)
PUTI t12
LI t13, 0
HALT

.section .strings
