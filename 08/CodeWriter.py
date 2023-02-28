"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    count_eq = 0
    count_lt = 0
    count_gt = 0

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.output_stream = output_stream
        self.filename = ''
        self.cur_func_name = ''
        self.count_call_in_cur_func = 0

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        self.filename = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        self.output_stream.write("\n//" + command + "\n")

        if command in {"add", "sub", "and", "or", "eq"}:
            self.output_stream.write("@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\n")

            if command in {"add", "sub", "and", "or"}:
                if command == "add":
                    self.output_stream.write("D=D+M\n")
                elif command == "sub":
                    self.output_stream.write("D=M-D\n")
                elif command == "and":
                    self.output_stream.write("D=D&M\n")
                elif command == "or":
                    self.output_stream.write("D=D|M\n")
                self.output_stream.write("@SP\nA=M\nM=D\n@SP\nM=M+1\n")

            elif command == "eq":
                self.output_stream.write("D=M-D\n@EQ_{0}\nD;JEQ\n@SP\nA=M\nM=0\n@SP\nM=M+1\n@END_EQ_{0}\n0;JMP\n"
                                         "(EQ_{0})\n@SP\nA=M\nM=-1\n@SP\nM=M+1\n(END_EQ_{0})\n".
                                         format(CodeWriter.count_eq))
                CodeWriter.count_eq += 1

        elif command == "gt":
            self.output_stream.write("@SP\nM=M-1\nA=M\nD=M\n@Y_IS_NEG_G_{0}\nD;JLT\n"
                                     "@SP\nM=M-1\nA=M\nD=M\n@SUBTRACT_G_{0}\nD;JGE\n"
                                     "@SP\nA=M\nM=0\n@SP\nM=M+1\n@END_GT_{0}\n0;JMP\n"
                                     "(Y_IS_NEG_G_{0})\n@SP\nM=M-1\nA=M\nD=M\n@SUBTRACT_G_{0}\nD;JLT\n"
                                     "@SP\nA=M\nM=-1\n@SP\nM=M+1\n@END_GT_{0}\n0;JMP\n"
                                     "(SUBTRACT_G_{0})\n@SP\nM=M+1\nA=M\nD=D-M\n@GT_{0}\nD;JGT\n"
                                     "@SP\nM=M-1\nA=M\nM=0\n@SP\nM=M+1\n@END_GT_{0}\n0;JMP\n"
                                     "(GT_{0})\n@SP\nM=M-1\nA=M\nM=-1\n@SP\nM=M+1\n(END_GT_{0})\n".
                                     format(CodeWriter.count_gt))
            CodeWriter.count_gt += 1

        elif command == "lt":
            self.output_stream.write("@SP\nM=M-1\nA=M\nD=M\n@Y_IS_NEG_L_{0}\nD;JLT\n"
                                     "@SP\nM=M-1\nA=M\nD=M\n@SUBTRACT_L_{0}\nD;JGE\n"
                                     "@SP\nA=M\nM=-1\n@SP\nM=M+1\n@END_LT_{0}\n0;JMP\n"
                                     "(Y_IS_NEG_L_{0})\n@SP\nM=M-1\nA=M\nD=M\n@SUBTRACT_L_{0}\nD;JLT\n"
                                     "@SP\nA=M\nM=0\n@SP\nM=M+1\n@END_LT_{0}\n0;JMP\n"
                                     "(SUBTRACT_L_{0})\n@SP\nM=M+1\nA=M\nD=D-M\n@LT_{0}\nD;JLT\n"
                                     "@SP\nM=M-1\nA=M\nM=0\n@SP\nM=M+1\n@END_LT_{0}\n0;JMP\n"
                                     "(LT_{0})\n@SP\nM=M-1\nA=M\nM=-1\n@SP\nM=M+1\n(END_LT_{0})\n".
                                     format(CodeWriter.count_lt))
            CodeWriter.count_lt += 1

        elif command == "not":
            self.output_stream.write("@SP\nM=M-1\nA=M\nM=!M\n@SP\nM=M+1\n")
        elif command == "shiftleft":
            self.output_stream.write("@SP\nM=M-1\nA=M\nM=M<<\n@SP\nM=M+1\n")
        elif command == "shiftright":
            self.output_stream.write("@SP\nM=M-1\nA=M\nM=M>>\n@SP\nM=M+1\n")
        elif command == "neg":
            self.output_stream.write("@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1\n")

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        self.output_stream.write("\n//" + command + " " + segment + " " + str(index) + "\n")
        push_template = "@{}\nA=M\nD=A\n@" + str(index) + "\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
        pop_template = "@{}\nD=M\n@" + str(index) + \
                       "\nD=D+A\n@SP\nA=M\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M+1\nA=M\nA=M\nM=D\n@SP\nM=M-1\n"
        if command == "C_PUSH":
            if segment == "constant":
                self.output_stream.write("@{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(str(index)))
            elif segment == "local":
                self.output_stream.write(push_template.format("LCL"))
            elif segment == "argument":
                self.output_stream.write(push_template.format("ARG"))
            elif segment == "this":
                self.output_stream.write(push_template.format("THIS"))
            elif segment == "that":
                self.output_stream.write(push_template.format("THAT"))
            elif segment == "temp":
                self.output_stream.write("@5\nD=A\n@" + str(index) + "\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == "pointer":
                if index == 0:
                    self.output_stream.write("@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
                elif index == 1:
                    self.output_stream.write("@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
            elif segment == "static":
                self.output_stream.write(
                    "@{}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n".format(self.filename + '.' + str(index)))

        elif command == "C_POP":
            if segment == "local":
                self.output_stream.write(pop_template.format("LCL"))
            elif segment == "argument":
                self.output_stream.write(pop_template.format("ARG"))
            elif segment == "this":
                self.output_stream.write(pop_template.format("THIS"))
            elif segment == "that":
                self.output_stream.write(pop_template.format("THAT"))
            elif segment == "temp":
                self.output_stream.write("@5\nD=A\n@" + str(index) + "\nD=D+A\n@SP\nA=M\nM=D\n@SP\nM=M-1\nA=M\nD=M\n"
                                                                     "@SP\nM=M+1\nA=M\nA=M\nM=D\n@SP\nM=M-1\n")
            elif segment == "pointer":
                if index == 0:
                    self.output_stream.write("@SP\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n")
                elif index == 1:
                    self.output_stream.write("@SP\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n")
            elif segment == "static":
                self.output_stream.write("@SP\nM=M-1\nA=M\nD=M\n@{}\nM=D\n".format(self.filename + '.' + str(index)))

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        self.output_stream.write("\n//label " + label + "\n")
        self.output_stream.write("(" + self.cur_func_name + "$" + label + ")\n")

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        self.output_stream.write("\n//goto " + label + "\n")
        self.output_stream.write("@" + self.cur_func_name + "$" + label + "\n0;JMP\n")

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        self.output_stream.write("\n//if-goto " + label + "\n")
        self.output_stream.write("@SP\nM=M-1\nA=M\nD=M\n@"
                                 + self.cur_func_name + "$" + label + "\nD;JNE\n")

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        self.cur_func_name = function_name
        self.count_call_in_cur_func = 0
        self.output_stream.write("\n//function " + function_name +  " " + str(n_vars) + "\n")
        self.output_stream.write("(" + function_name + ")\n")
        for _ in range(n_vars):
            self.output_stream.write("////push constant 0\n@0\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

    def _create_return_address(self):
        return self.cur_func_name + '$ret.' + str(self.count_call_in_cur_func)

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        self.count_call_in_cur_func += 1
        self.output_stream.write("\n//call " + function_name + " " + str(n_args) + "\n")
        self.output_stream.write("////push return_address\n@" + self._create_return_address() +
                                 "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.output_stream.write("////push LCL\n@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.output_stream.write("////push ARG\n@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.output_stream.write("////push THIS\n@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.output_stream.write("////push THAT\n@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        self.output_stream.write("////ARG = SP-5-n_args\n@SP\nD=M\n@5\nD=D-A\n@{}\nD=D-A\n@ARG\nM=D\n".format(str(n_args)))
        self.output_stream.write("////LCL = SP\n@SP\nD=M\n@LCL\nM=D\n")
        self.output_stream.write("////goto " + function_name + "\n@" + function_name + "\n0;JMP\n")
        self.output_stream.write("(" + self._create_return_address() + ")\n")

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        self.output_stream.write("\n//return\n")
        self.output_stream.write("////frame = LCL\n@LCL\nD=M\n@R13\nM=D\n")      # frame = RAM[13]
        self.output_stream.write("////return_address = *(frame-5)\n"
                                 "@R13\nD=M\n@5\nD=D-A\nA=D\nD=M\n@R14\nM=D\n")   # retAddress = RAM[14]
        self.output_stream.write("////*ARG = pop()\n@SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n")
        self.output_stream.write("////SP = ARG + 1\n@ARG\nD=M\nD=D+1\n@SP\nM=D\n")
        self.output_stream.write("////THAT = *(frame-1)\n@R13\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n")
        self.output_stream.write("////THIS = *(frame-2)\n@R13\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n")
        self.output_stream.write("////ARG = *(frame-3)\n@R13\nM=M-1\nA=M\nD=M\n@ARG\nM=D\n")
        self.output_stream.write("////LCL = *(frame-4)\n@R13\nM=M-1\nA=M\nD=M\n@LCL\nM=D\n")
        self.output_stream.write("////goto return_address\n@R14\nA=M\n0;JMP\n")

    def write_init(self):
        self.output_stream.write("//init\n@256\nD=A\n@SP\nM=D\n")
        self.write_call("Sys.init", 0)
