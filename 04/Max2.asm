@R1
D=M   //D=R1
@R2
D=D-M    //D=R1-R2
@BIGGER_R1    //if R1>=R2 Jump to BIGGER_R1
D;JGE
@R2   //R1<R2
D=M    //D=R2
@R0
M=D    //R0=R2
@END
0;JMP
(BIGGER_R1)   //if R1>=R2
@R1
D=M     //D=R1
@R0
M=D     //R0=R1
(END)
@END
0;JMP