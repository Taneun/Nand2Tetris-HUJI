// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
@R13
M=D
@Y_NEG_EQ_1
D;JLT
@SP
AM=M-1
D=M
@Y_POS_X_NEG_EQ_1
D;JLT
@R13
D=D-M
@CHECK_EQ_1
0;JMP
(Y_NEG_EQ_1)
@SP
AM=M-1
D=M
@Y_NEG_X_POS_EQ_1
D;JGT
@R13
D=D-M
@CHECK_EQ_1
0;JMP
(Y_POS_X_NEG_EQ_1)
D=-1
@CHECK_EQ_1
0;JMP
(Y_NEG_X_POS_EQ_1)
D=1
@CHECK_EQ_1
0;JMP
(CHECK_EQ_1)
@TRUE_EQ_1
D;JEQ
D=0
@CONTINUE_EQ_1
0;JMP
(TRUE_EQ_1)
D=-1
(CONTINUE_EQ_1)
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
AM=M-1
D=M
@R13
M=D
@Y_NEG_LT_2
D;JLT
@SP
AM=M-1
D=M
@Y_POS_X_NEG_LT_2
D;JLT
@R13
D=D-M
@CHECK_LT_2
0;JMP
(Y_NEG_LT_2)
@SP
AM=M-1
D=M
@Y_NEG_X_POS_LT_2
D;JGT
@R13
D=D-M
@CHECK_LT_2
0;JMP
(Y_POS_X_NEG_LT_2)
D=-1
@CHECK_LT_2
0;JMP
(Y_NEG_X_POS_LT_2)
D=1
@CHECK_LT_2
0;JMP
(CHECK_LT_2)
@TRUE_LT_2
D;JLT
D=0
@CONTINUE_LT_2
0;JMP
(TRUE_LT_2)
D=-1
(CONTINUE_LT_2)
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
@R13
M=D
@Y_NEG_GT_3
D;JLT
@SP
AM=M-1
D=M
@Y_POS_X_NEG_GT_3
D;JLT
@R13
D=D-M
@CHECK_GT_3
0;JMP
(Y_NEG_GT_3)
@SP
AM=M-1
D=M
@Y_NEG_X_POS_GT_3
D;JGT
@R13
D=D-M
@CHECK_GT_3
0;JMP
(Y_POS_X_NEG_GT_3)
D=-1
@CHECK_GT_3
0;JMP
(Y_NEG_X_POS_GT_3)
D=1
@CHECK_GT_3
0;JMP
(CHECK_GT_3)
@TRUE_GT_3
D;JGT
D=0
@CONTINUE_GT_3
0;JMP
(TRUE_GT_3)
D=-1
(CONTINUE_GT_3)
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 56
@56
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
// C_PUSH constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// neg
@SP
A=M-1
M=-M
// and
@SP
AM=M-1
D=M
A=A-1
M=D&M
// C_PUSH constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or
@SP
AM=M-1
D=M
A=A-1
M=D|M
