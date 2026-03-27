.section .text

MV fp, sp
JR func_main
HALT

func_main:
SW fp, 0(sp)
MV fp, sp
ADDI sp, sp, -4

GETI t0
LA t1, 0x20000000
SW t0, 0(t1)

GETI t2
LA t3, 0x20000004
SW t2, 0(t3)

LA t0, 0x20000000
LW t1, 0(t0)

LA t2, 0x20000004
LW t3, 0(t2)

;loaded the registers with the values just for the sake of practice (could have just used t0 and t2)

BLE t1, t3, elif
if:

LA t4, 0x10000028
PUTS t4
J finish

elif:
BLT t1, t3, else
LA t4, 0x10000014
PUTS t4
J finish

else:
LA t4, 0x10000000
PUTS t4

finish:

MV sp, fp
LW fp, 0(fp)
RET

.section .strings
0x10000000 "a is less than b\n"
0x10000014 "a is equal to b\n"
0x10000028 "a is greater than b\n"