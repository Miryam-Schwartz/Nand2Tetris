//init
@256
D=A
@SP
M=D

//call Sys.init 0
////push return_address
@$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
////push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
////push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
////push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
////push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
////ARG = SP-5-n_args
@SP
D=M
@5
D=D-A
@0
D=D-A
@ARG
M=D
////LCL = SP
@SP
D=M
@LCL
M=D
////goto Sys.init
@Sys.init
0;JMP
($ret.1)

//function Main.fibonacci 0
(Main.fibonacci)

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

//lt
@SP
M=M-1
A=M
D=M
@Y_IS_NEG_L_0
D;JLT
@SP
M=M-1
A=M
D=M
@SUBTRACT_L_0
D;JGE
@SP
A=M
M=-1
@SP
M=M+1
@END_LT_0
0;JMP
(Y_IS_NEG_L_0)
@SP
M=M-1
A=M
D=M
@SUBTRACT_L_0
D;JLT
@SP
A=M
M=0
@SP
M=M+1
@END_LT_0
0;JMP
(SUBTRACT_L_0)
@SP
M=M+1
A=M
D=D-M
@LT_0
D;JLT
@SP
M=M-1
A=M
M=0
@SP
M=M+1
@END_LT_0
0;JMP
(LT_0)
@SP
M=M-1
A=M
M=-1
@SP
M=M+1
(END_LT_0)

//if-goto IF_TRUE
@SP
M=M-1
A=M
D=M
@Main.fibonacci$IF_TRUE
D;JNE

//goto IF_FALSE
@Main.fibonacci$IF_FALSE
0;JMP

//label IF_TRUE
(Main.fibonacci$IF_TRUE)

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

//label IF_FALSE
(Main.fibonacci$IF_FALSE)

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

//call Main.fibonacci 1
////push return_address
@Main.fibonacci$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
////push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
////push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
////push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
////push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
////ARG = SP-5-n_args
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
////LCL = SP
@SP
D=M
@LCL
M=D
////goto Main.fibonacci
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.1)

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

//call Main.fibonacci 1
////push return_address
@Main.fibonacci$ret.2
D=A
@SP
A=M
M=D
@SP
M=M+1
////push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
////push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
////push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
////push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
////ARG = SP-5-n_args
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
////LCL = SP
@SP
D=M
@LCL
M=D
////goto Main.fibonacci
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.2)

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

//function Sys.init 0
(Sys.init)

//C_PUSH constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1

//call Main.fibonacci 1
////push return_address
@Sys.init$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
////push LCL
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
////push ARG
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
////push THIS
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
////push THAT
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
////ARG = SP-5-n_args
@SP
D=M
@5
D=D-A
@1
D=D-A
@ARG
M=D
////LCL = SP
@SP
D=M
@LCL
M=D
////goto Main.fibonacci
@Main.fibonacci
0;JMP
(Sys.init$ret.1)

//label WHILE
(Sys.init$WHILE)

//goto WHILE
@Sys.init$WHILE
0;JMP
