; a = 2, b = 3, a += a, a += b, b++, c = b, c--

START:
    LDC 2,RA
    LDC 3,RB
    ADD RA,RA
    ADD RB,RA

    NOP
    INC RB
    MOV RB,RC
    DEC RC
    JMP END

SKIPPED:
    CLR RA
    INC R0
    LDC 7,R1
    JMP SKIPPED

END:
    NOP
