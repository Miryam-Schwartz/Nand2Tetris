
//function SimpleFunction.test 2
(SimpleFunction.test)
////push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
////push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

//C_PUSH local 0
@LCL
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

//C_PUSH local 1
@LCL
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

//not
@SP
M=M-1
A=M
M=!M
@SP
M=M+1

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

//return
////frame = LCL
@LCL
D=M
@R13
M=D
////return_address = *(frame-5)
@R13
D=M
@5
D=D-A
A=D
D=M
@R14
M=D
////*ARG = pop()
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
////SP = ARG + 1
@ARG
D=M
D=D+1
@SP
M=D
////THAT = *(frame-1)
@R13
M=M-1
A=M
D=M
@THAT
M=D
////THIS = *(frame-2)
@R13
M=M-1
A=M
D=M
@THIS
M=D
////ARG = *(frame-3)
@R13
M=M-1
A=M
D=M
@ARG
M=D
////LCL = *(frame-4)
@R13
M=M-1
A=M
D=M
@LCL
M=D
////goto return_address
@R14
A=M
0;JMP
