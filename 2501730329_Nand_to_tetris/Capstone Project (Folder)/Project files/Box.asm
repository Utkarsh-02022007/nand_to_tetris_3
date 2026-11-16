// Utkarsh Yadav | 2501730329 | K = 29
// Box: row 29, 20 rows high, 32 pixels wide (2 screen words per row).
// Press any key to draw black; release all keys to clear the box.

(START)
    @KBD
    D=M
    @DRAW
    D;JNE
    @CLEAR
    0;JMP

(DRAW)
    @SCREEN
    D=A
    @928
    D=D+A
    @R13
    M=D
    @20
    D=A
    @R14
    M=D
(DRAW_ROW)
    @R13
    A=M
    M=-1
    A=A+1
    M=-1
    @30
    D=A
    @R13
    M=D+M
    @R14
    MD=M-1
    @DRAW_ROW
    D;JGT
    @START
    0;JMP

(CLEAR)
    @SCREEN
    D=A
    @928
    D=D+A
    @R13
    M=D
    @20
    D=A
    @R14
    M=D
(CLEAR_ROW)
    @R13
    A=M
    M=0
    A=A+1
    M=0
    @30
    D=A
    @R13
    M=D+M
    @R14
    MD=M-1
    @CLEAR_ROW
    D;JGT
    @START
    0;JMP
