//  init
@256
D=A
@SP
M=D
//  call Sys.init 0 args
@Sys.init$ret.0
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(Sys.init$ret.0)
//  function Sys.init 0 vars
(Sys.init)
// C_PUSH constant 4000
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP pointer 0
@SP
AM=M-1
D=M
@THIS
M=D
// C_PUSH constant 5000
@5000
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP pointer 1
@SP
AM=M-1
D=M
@THAT
M=D
//  call Sys.main 0 args
@Sys.main$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.main
0;JMP
(Sys.main$ret.1)
// C_POP temp 1
@SP
AM=M-1
D=M
@6
M=D
//  label LOOP
(Sys.init$LOOP)
//  goto LOOP
@Sys.init$LOOP
0;JMP
//  function Sys.main 5 vars
(Sys.main)
//  initializes 5 variables to 0
@SP
A=M
M=0
@SP
M=M+1
A=M
M=0
@SP
M=M+1
A=M
M=0
@SP
M=M+1
A=M
M=0
@SP
M=M+1
A=M
M=0
@SP
M=M+1
// C_PUSH constant 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP pointer 0
@SP
AM=M-1
D=M
@THIS
M=D
// C_PUSH constant 5001
@5001
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP pointer 1
@SP
AM=M-1
D=M
@THAT
M=D
// C_PUSH constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP local 1
@LCL
D=M
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// C_PUSH constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP local 2
@LCL
D=M
@2
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// C_PUSH constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP local 3
@LCL
D=M
@3
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// C_PUSH constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1
//  call Sys.add12 1 args
@Sys.add12$ret.2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.add12
0;JMP
(Sys.add12$ret.2)
// C_POP temp 0
@SP
AM=M-1
D=M
@5
M=D
// C_PUSH local 0
@LCL
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH local 1
@LCL
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH local 2
@LCL
D=M
@2
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH local 3
@LCL
D=M
@3
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH local 4
@LCL
D=M
@4
A=D+A
D=M
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
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
//  return
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
AM=M-1
D=M
@THAT
M=D
@R13
AM=M-1
D=M
@THIS
M=D
@R13
AM=M-1
D=M
@ARG
M=D
@R13
AM=M-1
D=M
@LCL
M=D
@R14
A=M
0;JMP
//  function Sys.add12 0 vars
(Sys.add12)
// C_PUSH constant 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP pointer 0
@SP
AM=M-1
D=M
@THIS
M=D
// C_PUSH constant 5002
@5002
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP pointer 1
@SP
AM=M-1
D=M
@THAT
M=D
// C_PUSH argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 12
@12
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
//  return
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
AM=M-1
D=M
@THAT
M=D
@R13
AM=M-1
D=M
@THIS
M=D
@R13
AM=M-1
D=M
@ARG
M=D
@R13
AM=M-1
D=M
@LCL
M=D
@R14
A=M
0;JMP
