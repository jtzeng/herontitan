; Test program that should do nothing and not be run.

.WORD HUE 0xFE5A
.WORD HUELL 0xFACE
.BYTE LOL 19
.DATA heheXD 1 2 3 4 5 4 3 0x2 0x1
.RAW 0xca 0xfe 0xba 0xbe
.ASCIZ MESSAGE "HELLO WORLD!!! <3"

.ASCIZ MSG " x  y   z    abc"

START:
    NOP
    HLT
    ADD R1,R7
    SUB R1,R1
    NOT R0
    INC R2

    INT 0xee

    PSH R2
    POP R2
    PKR R3

    CLR R3
    MOV R3,R0
    LDC 0xff,R5

; Infinite loop
LOOP:
    NOP
    JMP LOOP

WINK:
    JRA R5,R6
    JMP TEST
    RSB

TEST:
    JMO R1,R2,0xfedc

    ; Unclear spec order, so probably wrong?
    LDM 0xffff,R5
    LDR R3,R4,RA
    LMO R3,R4,0xbabe,R1

    STM R5,0xffff
    SRA RA,R3,R4
    SMO R1,R3,R4,0xbeef

    JMP HUE
