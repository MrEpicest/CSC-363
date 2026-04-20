; Symbol table GLOBAL
; Function: Type.INT foo([<Type.INT: 2>, <Type.INT: 2>])
; Function: Type.INT bar([<Type.INT: 2>, <Type.INT: 2>])
; Function: Type.INT main([])

; Symbol table main
; name a type Type.INT location -4
; name b type Type.INT location -8
; name c type Type.INT location -12
; name d type Type.INT location -16

; Symbol table foo
; name y type Type.INT location 12
; name x type Type.INT location 16

; Symbol table bar
; name y type Type.INT location 12
; name x type Type.INT location 16

.section .text
;Current temp: 
;IR Code: 
MV fp, sp
JR func_entry_main
HALT

func_entry_main:
SW fp, 0(sp)
MV fp, sp
ADDI sp, sp, -20
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
func_code_main:
GETI t0
SW t0, -4(fp)
GETI t1
SW t1, -8(fp)
LW t2, -4(fp)
SW t2, 0(sp)
ADDI sp, sp, -4
LW t3, -8(fp)
SW t3, 0(sp)
ADDI sp, sp, -4
ADDI sp, sp, -4
SW ra, 0(sp)
ADDI sp, sp, -4
JR func_entry_foo
ADDI sp, sp, 4
LW ra, 0(sp)
ADDI sp, sp, 4
LW t4, 0(sp)
ADDI sp, sp, 8
SW t4, -12(fp)
LW t5, -4(fp)
SW t5, 0(sp)
ADDI sp, sp, -4
LW t6, -8(fp)
SW t6, 0(sp)
ADDI sp, sp, -4
ADDI sp, sp, -4
SW ra, 0(sp)
ADDI sp, sp, -4
JR func_entry_bar
ADDI sp, sp, 4
LW ra, 0(sp)
ADDI sp, sp, 4
LW t7, 0(sp)
ADDI sp, sp, 8
SW t7, -16(fp)
LW t8, -12(fp)
PUTI t8
LW t9, -16(fp)
PUTI t9
LI t10, 0
SW t10, 8(fp)
func_ret_main:
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
ADDI sp, sp, -4
SW t0, 0(sp)
ADDI sp, sp, -4
SW t1, 0(sp)
ADDI sp, sp, -4
SW t2, 0(sp)
ADDI sp, sp, -4
func_code_foo:
LW t0, 16(fp)
LW t1, 12(fp)
ADD t2, t0, t1
SW t2, 8(fp)
func_ret_foo:
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

func_entry_bar:
SW fp, 0(sp)
MV fp, sp
ADDI sp, sp, -4
SW t0, 0(sp)
ADDI sp, sp, -4
SW t1, 0(sp)
ADDI sp, sp, -4
SW t2, 0(sp)
ADDI sp, sp, -4
func_code_bar:
LW t0, 16(fp)
LW t1, 12(fp)
SUB t2, t0, t1
SW t2, 8(fp)
func_ret_bar:
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
