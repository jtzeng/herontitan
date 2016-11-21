# herontitan
herontitan is a WIP assembler for bootnecklad's "Titan" processor.

The specifications are located here: https://github.com/bootnecklad/Titan-Specifications

Usage
-----

```
usage: herontitan.py [-h] [-d] [-b] [-t] inputfile

positional arguments:
  inputfile    path to input source file

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  print all parsing steps
  -b, --bin    print result in binary format
  -t, --text   print result as human-readable binary text with \n separators
  ```

The default output format is a comma-separated list of bytes in decimal. 😁

Example
-------

```asm
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
```

```
$ python herontitan.py ./ex/testadd2.asm
[170, 2, 171, 3, 16, 170, 16, 186, 0, 24, 176, 144, 188, 25, 192, 176, 0, 26, 138, 24, 0, 161, 7, 176, 0, 18, 0]
```

```
$ python herontitan.py ./ex/testadd2.asm --text
10101010
00000010
10101011
00000011
00010000
10101010
00010000
10111010
00000000
00011000
10110000
10010000
10111100
00011001
11000000
10110000
00000000
00011010
10001010
00011000
00000000
10100001
00000111
10110000
00000000
00010010
00000000
```
