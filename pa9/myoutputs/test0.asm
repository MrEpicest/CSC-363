; Symbol table 
; name true type Type.STRING location 0x10000000 value "True\n"
; name false type Type.STRING location 0x10000004 value "False\n"
; name a type Type.FLOAT location 0x20000000
; name b type Type.FLOAT location 0x20000004

.section .text
;Current temp: 
;IR Code: 
FIMM.S f1, 3.0
LA t1, 0x20000000
FSW f1, 0(t1)
FIMM.S f2, 2.0
LA t2, 0x20000004
FSW f2, 0(t2)
LA t3, 0x20000000
FLW f3, 0(t3)
LA t4, 0x20000004
FLW f4, 0(t4)
; Left type: Type.FLOAT
; Right type: Type.FLOAT
FLT.S t5, f3, f4
BNE t5, x0, else0
then0:
LA t6, 0x10000000
PUTS t6
J done0
else0:
LA t7, 0x10000004
PUTS t7
done0:
LI t8, 0
HALT

.section .strings
0x10000000 "True\n"
0x10000004 "False\n"
