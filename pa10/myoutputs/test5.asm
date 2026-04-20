; Symbol table GLOBAL
; name curVal type Type.FLOAT location 0x20000000
; name x type Type.FLOAT location 0x20000004
; name degree type Type.INT location 0x20000008
; Function: Type.FLOAT poly([<Type.FLOAT: 3>, <Type.FLOAT: 3>, <Type.INT: 2>])
; name val type Type.STRING location 0x10000000 value "Enter x value to evaluate: "
; name degreePrompt type Type.STRING location 0x10000004 value "Enter a degree: "
; name prompt type Type.STRING location 0x10000008 value "Enter coefficient: "
; Function: Type.INT main([])

; Symbol table main
; name cur type Type.INT location -4

; Symbol table poly
; name degree type Type.INT location 12
; name x type Type.FLOAT location 16
; name curVal type Type.FLOAT location 20
; name coeff type Type.FLOAT location -4

.section .text
;Current temp: 
;IR Code: 
MV fp, sp
JR func_entry_main
HALT

func_entry_main:
SW fp, 0(sp)
MV fp, sp
ADDI sp, sp, -8
SW t0, 0(sp)
ADDI sp, sp, -4
SW t1, 0(sp)
ADDI sp, sp, -4
SW t2, 0(sp)
ADDI sp, sp, -4
SW t3, 0(sp)
ADDI sp, sp, -4
SW t4, 0(sp)
ADDI sp, sp, -4
SW t5, 0(sp)
ADDI sp, sp, -4
SW t6, 0(sp)
ADDI sp, sp, -4
SW t7, 0(sp)
ADDI sp, sp, -4
SW t8, 0(sp)
ADDI sp, sp, -4
SW t9, 0(sp)
ADDI sp, sp, -4
SW t10, 0(sp)
ADDI sp, sp, -4
SW t11, 0(sp)
ADDI sp, sp, -4
SW t12, 0(sp)
ADDI sp, sp, -4
SW t13, 0(sp)
ADDI sp, sp, -4
FSW f0, 0(sp)
ADDI sp, sp, -4
FSW f1, 0(sp)
ADDI sp, sp, -4
FSW f2, 0(sp)
ADDI sp, sp, -4
FSW f3, 0(sp)
ADDI sp, sp, -4
FSW f4, 0(sp)
ADDI sp, sp, -4
FSW f5, 0(sp)
ADDI sp, sp, -4
func_code_main:
FIMM.S f0, 0.0
LA t0, 0x20000000
FSW f0, 0(t0)
LI t1, 0
SW t1, -4(fp)
LA t2, 0x10000000
PUTS t2
GETF f1
LA t3, 0x20000004
FSW f1, 0(t3)
LA t4, 0x10000004
PUTS t4
GETI t5
LA t6, 0x20000008
SW t5, 0(t6)
LA t7, 0x20000000
FLW f2, 0(t7)
SW f2, 0(sp)
ADDI sp, sp, -4
LA t8, 0x20000004
FLW f3, 0(t8)
SW f3, 0(sp)
ADDI sp, sp, -4
LA t9, 0x20000008
LW t10, 0(t9)
SW t10, 0(sp)
ADDI sp, sp, -4
ADDI sp, sp, -4
SW ra, 0(sp)
ADDI sp, sp, -4
JR func_entry_poly
ADDI sp, sp, 4
LW ra, 0(sp)
ADDI sp, sp, 4
FLW f4, 0(sp)
ADDI sp, sp, 12
LA t11, 0x20000000
FSW f4, 0(t11)
LA t12, 0x20000000
FLW f5, 0(t12)
PUTF f5
LI t13, 0
SW t13, 8(fp)
func_ret_main:
ADDI sp, sp, 4
FLW f5, 0(sp)
ADDI sp, sp, 4
FLW f4, 0(sp)
ADDI sp, sp, 4
FLW f3, 0(sp)
ADDI sp, sp, 4
FLW f2, 0(sp)
ADDI sp, sp, 4
FLW f1, 0(sp)
ADDI sp, sp, 4
FLW f0, 0(sp)
ADDI sp, sp, 4
LW t13, 0(sp)
ADDI sp, sp, 4
LW t12, 0(sp)
ADDI sp, sp, 4
LW t11, 0(sp)
ADDI sp, sp, 4
LW t10, 0(sp)
ADDI sp, sp, 4
LW t9, 0(sp)
ADDI sp, sp, 4
LW t8, 0(sp)
ADDI sp, sp, 4
LW t7, 0(sp)
ADDI sp, sp, 4
LW t6, 0(sp)
ADDI sp, sp, 4
LW t5, 0(sp)
ADDI sp, sp, 4
LW t4, 0(sp)
ADDI sp, sp, 4
LW t3, 0(sp)
ADDI sp, sp, 4
LW t2, 0(sp)
ADDI sp, sp, 4
LW t1, 0(sp)
ADDI sp, sp, 4
LW t0, 0(sp)
ADDI sp, sp, 4
MV sp, fp
LW fp, 0(fp)
RET

func_entry_poly:
SW fp, 0(sp)
MV fp, sp
ADDI sp, sp, -8
SW t0, 0(sp)
ADDI sp, sp, -4
SW t1, 0(sp)
ADDI sp, sp, -4
SW t2, 0(sp)
ADDI sp, sp, -4
SW t3, 0(sp)
ADDI sp, sp, -4
SW t4, 0(sp)
ADDI sp, sp, -4
SW t5, 0(sp)
ADDI sp, sp, -4
FSW f0, 0(sp)
ADDI sp, sp, -4
FSW f1, 0(sp)
ADDI sp, sp, -4
FSW f2, 0(sp)
ADDI sp, sp, -4
FSW f3, 0(sp)
ADDI sp, sp, -4
FSW f4, 0(sp)
ADDI sp, sp, -4
FSW f5, 0(sp)
ADDI sp, sp, -4
FSW f6, 0(sp)
ADDI sp, sp, -4
FSW f7, 0(sp)
ADDI sp, sp, -4
FSW f8, 0(sp)
ADDI sp, sp, -4
func_code_poly:
LW t1, 12(fp)
LI t0, 0
BLE t1, t0, else1
then1:
FLW f0, 20(fp)
SW f0, 0(sp)
ADDI sp, sp, -4
FLW f1, 16(fp)
SW f1, 0(sp)
ADDI sp, sp, -4
LW t3, 12(fp)
LI t2, 1
SUB t4, t3, t2
SW t4, 0(sp)
ADDI sp, sp, -4
ADDI sp, sp, -4
SW ra, 0(sp)
ADDI sp, sp, -4
JR func_entry_poly
ADDI sp, sp, 4
LW ra, 0(sp)
ADDI sp, sp, 4
FLW f2, 0(sp)
ADDI sp, sp, 12
FSW f2, 20(fp)
J done1
else1:
done1:
LA t5, 0x10000008
PUTS t5
GETF f3
FSW f3, -4(fp)
FLW f4, 16(fp)
FLW f5, 20(fp)
FMUL.S f6, f4, f5
FLW f7, -4(fp)
FADD.S f8, f6, f7
FSW f8, 8(fp)
func_ret_poly:
ADDI sp, sp, 4
FLW f8, 0(sp)
ADDI sp, sp, 4
FLW f7, 0(sp)
ADDI sp, sp, 4
FLW f6, 0(sp)
ADDI sp, sp, 4
FLW f5, 0(sp)
ADDI sp, sp, 4
FLW f4, 0(sp)
ADDI sp, sp, 4
FLW f3, 0(sp)
ADDI sp, sp, 4
FLW f2, 0(sp)
ADDI sp, sp, 4
FLW f1, 0(sp)
ADDI sp, sp, 4
FLW f0, 0(sp)
ADDI sp, sp, 4
LW t5, 0(sp)
ADDI sp, sp, 4
LW t4, 0(sp)
ADDI sp, sp, 4
LW t3, 0(sp)
ADDI sp, sp, 4
LW t2, 0(sp)
ADDI sp, sp, 4
LW t1, 0(sp)
ADDI sp, sp, 4
LW t0, 0(sp)
ADDI sp, sp, 4
MV sp, fp
LW fp, 0(fp)
RET


.section .strings
0x10000000 "Enter x value to evaluate: "
0x10000004 "Enter a degree: "
0x10000008 "Enter coefficient: "
