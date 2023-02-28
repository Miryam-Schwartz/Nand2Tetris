
//C_PUSH argument 1
@ARG
A=M
D=A
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

//C_POP pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D

//C_PUSH constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

//C_POP that 0
@THAT
D=M
@0
D=D+A
@SP
A=M
M=D
@SP
M=M-1
A=M
D=M
@SP
M=M+1
A=M
A=M
M=D
@SP
M=M-1

//C_PUSH constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

//C_POP that 1
@THAT
D=M
@1
D=D+A
@SP
A=M
M=D
@SP
M=M-1
A=M
D=M
@SP
M=M+1
A=M
A=M
M=D
@SP
M=M-1

//C_PUSH argument 0
@ARG
A=M
D=A
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

//C_PUSH constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

//sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@SP
A=M
M=D
@SP
M=M+1

//C_POP argument 0
@ARG
D=M
@0
D=D+A
@SP
A=M
M=D
@SP
M=M-1
A=M
D=M
@SP
M=M+1
A=M
A=M
M=D
@SP
M=M-1

//label MAIN_LOOP_START
(FibonacciSeries.$MAIN_LOOP_START)

//C_PUSH argument 0
@ARG
A=M
D=A
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

//if-goto COMPUTE_ELEMENT
@SP
M=M-1
A=M
D=M
@FibonacciSeries.$COMPUTE_ELEMENT
D;JGT

//goto END_PROGRAM
@FibonacciSeries.$END_PROGRAM
0;JMP

//label COMPUTE_ELEMENT
(FibonacciSeries.$COMPUTE_ELEMENT)

//C_PUSH that 0
@THAT
A=M
D=A
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

//C_PUSH that 1
@THAT
A=M
D=A
@1
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

//add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D+M
@SP
A=M
M=D
@SP
M=M+1

//C_POP that 2
@THAT
D=M
@2
D=D+A
@SP
A=M
M=D
@SP
M=M-1
A=M
D=M
@SP
M=M+1
A=M
A=M
M=D
@SP
M=M-1

//C_PUSH pointer 1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

//C_PUSH constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

//add
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D+M
@SP
A=M
M=D
@SP
M=M+1

//C_POP pointer 1
@SP
M=M-1
A=M
D=M
@THAT
M=D

//C_PUSH argument 0
@ARG
A=M
D=A
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

//C_PUSH constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

//sub
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=M-D
@SP
A=M
M=D
@SP
M=M+1

//C_POP argument 0
@ARG
D=M
@0
D=D+A
@SP
A=M
M=D
@SP
M=M-1
A=M
D=M
@SP
M=M+1
A=M
A=M
M=D
@SP
M=M-1

//goto MAIN_LOOP_START
@FibonacciSeries.$MAIN_LOOP_START
0;JMP

//label END_PROGRAM
(FibonacciSeries.$END_PROGRAM)
