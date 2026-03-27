.section .text

MV fp, sp
JR func_main
HALT

func_main:
SW fp, 0(sp)
MV fp, sp
ADDI sp, sp, -4

ADDI sp, sp, -4
ADDI sp, sp, -4

LI t0, 0
SW t0, -4(fp)

LI t1, 0
SW t1, -8(fp)

while1:
LW t0, -4(fp)
LI t1, 0
BGT t0, t1, finish1

LA t1, 0x10000000
PUTS t1
GETI t2
SW t2, -4(fp)
J while1

finish1:


while2:
LW t0, -4(fp)
LI t1, 1
BLE t0, t1, finish2

LW t2, -4(fp)

PUTI t2

LW t2, -4(fp)
LI t3, 2
DIV t2, t2, t3
MUL t2, t2, t3
SUB t2, t0, t2
LI t3, 0

BNE t2, t3, else
if:

LW t4, -4(fp)
LI t5, 2
DIV t4, t4, t5
SW t4, -4(fp)

LW t6, -8(fp)
ADDI t6, t6, 1
SW t6, -8(fp)

J postif

else:

LW t4, -4(fp)
LI t5, 3
MUL t4, t4, t5
ADDI t4, t4, 1
SW t4, -4(fp)

LW t6, -8(fp)
ADDI t6, t6, 1
SW t6, -8(fp)

postif:

J while2

finish2:

LW t0, -4(fp)
PUTI t0

LW t1, -8(fp)
PUTI t1

MV sp, fp
LW fp, 0(fp)
RET

.section .strings
0x10000000 "Please enter a positive integer\n"