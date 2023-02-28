// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.


//min_adress=R14
@R14
D=M
@min_adress
M=D

//max_adress=R14
@R14
D=M
@max_adress
M=D

//i=1
@i
M=1


(LOOP)
	//if (i>=R15) goto SWAP
	@i
	D=M
	@R15
	D=D-M
	@SWAP
	D; JGE
	
	//if RAM[R14+i] < RAM[min_adress] goto ASSIGN_MIN
	@min_adress
	D=M
	A=D
	D=M     //D=RAM[min_adress]
	@temp
	M=D     //temp=RAM[min_adress]
	@R14
	D=M
	@i
	D=D+M   //D=R14+i
	A=D
	D=M     //D=RAM[R14+i]
	@temp
	D=D-M   //D=RAM[R14+i]-RAM[min_adress]
	@ASSIGN_MIN
	D; JLT
	
	//if RAM[R14+i] > RAM[max_adress] goto ASSIGN_MAX
	@max_adress
	D=M
	A=D
	D=M     //D=RAM[max_adress]
	@temp
	M=D     //temp=RAM[max_adress]
	@R14
	D=M
	@i
	D=D+M   //D=R14+i
	A=D
	D=M     //D=RAM[R14+i]
	@temp
	D=D-M   //D=RAM[R14+i]-RAM[max_adress]
	@ASSIGN_MAX
	D; JGT
	
	
(LOOP_END)
	//i=i+1
	@i
	M=M+1
	
	//goto LOOP
	@LOOP
	0;JMP
	
	
(ASSIGN_MIN)
	@R14
	D=M
	@i
	D=D+M    //D=R14+i
	@min_adress
	M=D
	@LOOP_END
	0;JMP
	
(ASSIGN_MAX)
	@R14
	D=M
	@i
	D=D+M   //D=R14+i
	@max_adress
	M=D
	@LOOP_END
	0;JMP
	
(SWAP)

	//temp=RAM[min_adress]
	@min_adress
	A=M
	D=M     //D=RAM[min_adress]
	@temp
	M=D     //temp=RAM[min_adress]
	
	//RAM[min_adress] = RAM[max_adress]
	@max_adress
	A=M
	D=M     //D holds the max element
	@min_adress
	A=M
	M=D
	
	//RAM[max_adress] = temp
	@temp
	D=M     //D holds the min element
	@max_adress
	A=M
	M=D
	
(END)
	@END
	0; JMP
	
	
	
	
	
	