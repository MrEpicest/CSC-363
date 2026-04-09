; Symbol table 
; name i type Type.INT location 0x20000000

.section .text
;Current temp: 
;IR Code: 
LI t1, 1
LI t2, 0
BLE t1, t2, else2
then2:
LI t3, 2
LI t4, 1
BLE t3, t4, else1
then1:
LI t5, 0
LA t6, 0x20000000
SW t5, 0(t6)
J done1
else1:
done1:
J done2
else2:
done2:
LI t7, 0
HALT

.section .strings
