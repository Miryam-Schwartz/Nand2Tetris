
//function Sys.init 0
(Sys.init)

//C_PUSH constant 4000
@4000
D=A
@SP
A=M
M=D
@SP
M=M+1

//C_POP pointer 0
@SP
M=M-1
A=M
D=M
@THIS
M=D

//C_PUSH constant 5000
@5000
D=A
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

//call Sys.main 0
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
@0
D=D-A
@ARG
M=D
////LCL = SP
@SP
D=M
@LCL
M=D
////goto Sys.main
@Sys.main
0;JMP
(Sys.init$ret.1)

//C_POP temp 1
@5
D=A
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

//label LOOP
(Sys.init$LOOP)

//goto LOOP
@Sys.init$LOOP
0;JMP

//function Sys.main 5
(Sys.main)
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
////push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

//C_PUSH constant 4001
@4001
D=A
@SP
A=M
M=D
@SP
M=M+1

//C_POP pointer 0
@SP
M=M-1
A=M
D=M
@THIS
M=D

//C_PUSH constant 5001
@5001
D=A
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

//C_PUSH constant 200
@200
D=A
@SP
A=M
M=D
@SP
M=M+1

//C_POP local 1
@LCL
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

//C_PUSH constant 40
@40
D=A
@SP
A=M
M=D
@SP
M=M+1

//C_POP local 2
@LCL
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

//C_PUSH constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1

//C_POP local 3
@LCL
D=M
@3
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

//C_PUSH constant 123
@123
D=A
@SP
A=M
M=D
@SP
M=M+1

//call Sys.add12 1
////push return_address
@Sys.main$ret.1
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
////goto Sys.add12
@Sys.add12
0;JMP
(Sys.main$ret.1)

//C_POP temp 0
@5
D=A
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

//C_PUSH local 2
@LCL
A=M
D=A
@2
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

//C_PUSH local 3
@LCL
A=M
D=A
@3
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

//C_PUSH local 4
@LCL
A=M
D=A
@4
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

//function Sys.add12 0
(Sys.add12)

//C_PUSH constant 4002
@4002
D=A
@SP
A=M
M=D
@SP
M=M+1

//C_POP pointer 0
@SP
M=M-1
A=M
D=M
@THIS
M=D

//C_PUSH constant 5002
@5002
D=A
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

//C_PUSH constant 12
@12
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
