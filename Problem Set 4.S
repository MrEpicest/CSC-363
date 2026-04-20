#a
MV fp, sp
JR func_main
HALT

#b
func_bar:
SW fp, 0(sp)
MV fp, sp
ADDI sp, sp, -4
ADDI sp, sp, -4 # allocate space for local e
SW r0, 0(sp)
ADDI sp, sp, -4
SW r1, 0(sp)
ADDI sp, sp, -4
SW r2, 0(sp)
ADDI sp, sp, -4
SW r3, 0(sp)
ADDI sp, sp, -4
LW r0, 16(fp)
LW r1, 12(fp)
ADD r2, r0, r1
SW r2, -4(fp)
LW r3, -4(fp)
SW r3, 8(fp)
J func_ret_bar
func_ret_bar:
ADDI sp, sp 4
LW r3, 0(sp)
ADDI sp, sp 4
LW r2, 0(sp)
ADDI sp, sp 4
LW r1, 0(sp)
ADDI sp, sp 4
LW r0, 0(sp)
MV sp, fp
LW fp, 0(fp)
RET

#c
func_main:
SW fp, 0(sp)
MV fp, sp
ADDI sp, sp, -4
SW r0, 0(sp)
ADDI sp, sp, -4
SW r1, 0(sp)
ADDI sp, sp, -4
SW r2, 0(sp)
ADDI sp, sp, -4
SW r3, 0(sp)
ADDI sp, sp, -4
LI r0, 6
SW r0, 0(sp)
ADDI sp, sp, -4
LI r1, 7
SW r1, 0(sp)
ADDI sp, sp, -4
ADDI sp, sp, -4 # allocate space for return value
SW ra, 0(sp)
ADDI sp, sp, -4
JR foo
ADDI sp, sp, 4 # increment to stored ra of stub
LW ra, 0(sp)
ADDI sp, sp, 4 # increment to rv of foo
LW r2, 0(sp) # get the return value of foo into temp
ADDI sp, sp, 8 # increment to top parameter
LA r3, 0x200000000 # get address of global c
SW r2, 0(r3) # store return of foo in global c
# technically want to reload value of c into temp here (but I'm out of temps)
SW r2, 8(fp) # store global c as return of main
JR func_ret_main
func_ret_main:
ADDI sp, sp, 4
LW r3, 0(sp)
ADDI sp, sp 4
LW r2, 0(sp)
ADDI sp, sp 4
LW r1, 0(sp)
ADDI sp, sp 4
LW r0, 0(sp)
MV sp, fp
LW fp, 0(fp)
RET

#d
func_foo:
SW fp, 0(sp)
MV fp, sp
ADDI sp, sp -4
ADDI sp, sp -4 # allocate space for local d
SW r0, 0(sp) # store temps...
ADDI sp, sp, -4
SW r1, 0(sp)
ADDI sp, sp, -4
SW r2, 0(sp)
ADDI sp, sp, -4
SW r3, 0(sp) # ...store temps
ADDI sp, sp, -4
LW r0, 16(fp) # get value of param a of foo
SW r0, 0(sp) # store arg a for bar
ADDI sp, sp -4
LW r1, 12(fp) # get value of param b of foo
SW r1, 0(sp) # store arg b for bar
ADDI sp, sp, -4
ADDI sp, sp, -4 # allocate space for rv of bar
SW ra, 0(sp) # store ra of previous caller
ADDI sp, sp, -4
JR func_bar
ADDI sp, sp 4 # increment to stored ra of previous caller
LW ra, 0(sp)
ADDI sp, sp, 4 # increment to rv of bar
LW r2, 0(sp) # load rv of bar into temp
ADDI sp, sp, 8 #increment to top arg of bar
# technically want to reload params a and b to pass as arguments but I'm out of registers again
SW r0, 0(sp) # store arg a for bar
ADDI sp, sp, -4
SW r1, 0(sp) # store arg b for bar
ADDI sp, sp, -4
ADDI sp, sp, -4 # allocate space for rv of bar
SW ra, 0(sp) # store ra of previous caller
ADDI sp, sp -4
JR bar
ADDI sp, sp, 4 # increment to ra of previous caller
LW ra, 0(sp)
ADDI sp, sp, 4 # increment to rv of bar
LW r3, 0(sp)
ADDI sp, sp, 8 # increment to top arg of bar
MUL r0, r0, r2 # a*(return of bar) -- out of new registers to store to
MUL r1, r1, r3 # b*(return of bar) -- out of new registers to store to
ADD r0, r0, r1
SW r0, -4(fp) # save result to local d
# technically want to reload value of d into new temp
SW r0, 8(fp) # store d as rv of foo
JR func_ret_foo
func_ret_foo:
ADDI sp, sp, 4 # increment to bottom of stored registers
LW r3, 0(sp) # restore registers...
ADDI sp, sp, 4
LW r2, 0(sp)
ADDI sp, sp, 4
LW r1, 0(sp)
ADDI sp, sp, 4
LW r0, 0(sp) # ...restore registers
MV sp, fp
LW fp (fp)
RET