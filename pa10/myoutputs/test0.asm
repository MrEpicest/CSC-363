; Symbol table GLOBAL
; name true type Type.STRING location 0x10000000 value "True\n"
; name false type Type.STRING location 0x10000004 value "False\n"
; name a type Type.FLOAT location 0x20000000
; name b type Type.FLOAT location 0x20000004
; Function: Type.INT main([])
; Function: Type.FLOAT foo([<Type.INT: 2>, <Type.FLOAT: 3>])

; Symbol table main
; name c type Type.INT location -4
; name d type Type.INT location -8

; Symbol table foo
; name y type Type.FLOAT location 12
; name x type Type.INT location 16
; name d type Type.INT location -4
; name f type Type.FLOAT location -8
; name a type Type.FLOAT location -12

.section .text
;Current temp: 
;IR Code: 
MV fp, sp
JR func_entry_main
HALT

func_entry_main:
SW fp, 0(sp)
MV fp, sp
ADDI sp, sp, -12
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
func_code_main:
FIMM.S f0, 3.0
LA t0, 0x20000000
FSW f0, 0(t0)
FIMM.S f1, 2.0
LA t1, 0x20000004
FSW f1, 0(t1)
LI t2, 7
SW t2, -4(fp)
LW t4, -4(fp)
LI t3, 2
MUL t5, t4, t3
SW t5, -8(fp)
LA t6, 0x20000000
FLW f2, 0(t6)
LA t7, 0x20000004
FLW f3, 0(t7)
FLT.S t12, f2, f3
BNE t12, x0, else1
then1:
LW t8, -8(fp)
PUTI t8
LA t9, 0x10000000
PUTS t9
J done1
else1:
LW t10, -8(fp)
PUTI t10
LA t11, 0x10000004
PUTS t11
done1:
LI t13, 0
SW t13, 8(fp)
func_ret_main:
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

func_entry_foo:
SW fp, 0(sp)
MV fp, sp
ADDI sp, sp, -16
FSW f0, 0(sp)
ADDI sp, sp, -4
FSW f1, 0(sp)
ADDI sp, sp, -4
FSW f2, 0(sp)
ADDI sp, sp, -4
func_code_foo:
FLW f1, 12(fp)
FIMM.S f0, 1.0
FADD.S f2, f1, f0
SW f2, 8(fp)
func_ret_foo:
ADDI sp, sp, 4
FLW f2, 0(sp)
ADDI sp, sp, 4
FLW f1, 0(sp)
ADDI sp, sp, 4
FLW f0, 0(sp)
ADDI sp, sp, 4
MV sp, fp
LW fp, 0(fp)
RET


.section .strings
0x10000000 "True\n"
0x10000004 "False\n"
