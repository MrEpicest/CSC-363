; Symbol table 
; name i type Type.INT location 0x20000000
; name j type Type.INT location 0x20000004
; name max type Type.INT location 0x20000008
; name val type Type.INT location 0x2000000c
; name is type Type.STRING location 0x10000000 value "i: "
; name js type Type.STRING location 0x10000004 value "j: "
; name newline type Type.STRING location 0x10000008 value "\n"

.section .text
;Current temp: 
;IR Code: 
LI t1, 0
LA t2, 0x2000000c
SW t1, 0(t2)
GETI t3
LA t4, 0x20000008
SW t3, 0(t4)
LI t5, 0
LA t6, 0x20000000
SW t5, 0(t6)
loop2:
LA t7, 0x20000000
LW t8, 0(t7)
LA t9, 0x20000008
LW t10, 0(t9)
; Left type: Type.INT
; Right type: Type.INT
BGE t8, t10, else1
LA t11, 0x10000000
PUTS t11
LA t12, 0x20000000
LW t13, 0(t12)
PUTI t13
LA t14, 0x10000008
PUTS t14
LA t15, 0x20000000
LW t16, 0(t15)
LA t17, 0x20000004
SW t16, 0(t17)
loop2:
LA t18, 0x20000004
LW t19, 0(t18)
LA t20, 0x20000008
LW t21, 0(t20)
; Left type: Type.INT
; Right type: Type.INT
BGE t19, t21, else2
LA t22, 0x10000004
PUTS t22
LA t23, 0x20000004
LW t24, 0(t23)
PUTI t24
LA t25, 0x10000008
PUTS t25
LA t27, 0x2000000c
LW t28, 0(t27)
LI t26, 1
ADD t29, t28, t26
LA t30, 0x2000000c
SW t29, 0(t30)
LA t32, 0x20000004
LW t33, 0(t32)
LI t31, 1
ADD t34, t33, t31
LA t35, 0x20000004
SW t34, 0(t35)
J loop2
else2:
done2:
LA t37, 0x20000000
LW t38, 0(t37)
LI t36, 1
ADD t39, t38, t36
LA t40, 0x20000000
SW t39, 0(t40)
J loop2
else2:
done2:
LA t41, 0x2000000c
LW t42, 0(t41)
PUTI t42
LI t43, 0
HALT

.section .strings
0x10000000 "i: "
0x10000004 "j: "
0x10000008 "\n"
