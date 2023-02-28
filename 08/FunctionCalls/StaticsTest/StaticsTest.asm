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

//function Class1.set 0
(Class1.set)

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

//C_POP static 0
@SP
M=M-1
A=M
D=M
@Class1.0
M=D

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

//C_POP static 1
@SP
M=M-1
A=M
D=M
@Class1.1
M=D

//C_PUSH constant 0
@0
D=A
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

//function Class1.get 0
(Class1.get)

//C_PUSH static 0
@Class1.0
D=M
@SP
A=M
M=D
@SP
M=M+1

//C_PUSH static 1
@Class1.1
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

//function Class2.set 0
(Class2.set)

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

//C_POP static 0
@SP
M=M-1
A=M
D=M
@Class2.0
M=D

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

//C_POP static 1
@SP
M=M-1
A=M
D=M
@Class2.1
M=D

//C_PUSH constant 0
@0
D=A
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

//function Class2.get 0
(Class2.get)

//C_PUSH static 0
@Class2.0
D=M
@SP
A=M
M=D
@SP
M=M+1

//C_PUSH static 1
@Class2.1
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

//function Sys.init 0
(Sys.init)

//C_PUSH constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1

//C_PUSH constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1

//call Class1.set 2
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
@2
D=D-A
@ARG
M=D
////LCL = SP
@SP
D=M
@LCL
M=D
////goto Class1.set
@Class1.set
0;JMP
(Sys.init$ret.1)

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

//C_PUSH constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1

//C_PUSH constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1

//call Class2.set 2
////push return_address
@Sys.init$ret.2
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
@2
D=D-A
@ARG
M=D
////LCL = SP
@SP
D=M
@LCL
M=D
////goto Class2.set
@Class2.set
0;JMP
(Sys.init$ret.2)

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

//call Class1.get 0
////push return_address
@Sys.init$ret.3
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
////goto Class1.get
@Class1.get
0;JMP
(Sys.init$ret.3)

//call Class2.get 0
////push return_address
@Sys.init$ret.4
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
////goto Class2.get
@Class2.get
0;JMP
(Sys.init$ret.4)

//label WHILE
(Sys.init$WHILE)

//goto WHILE
@Sys.init$WHILE
0;JMP
