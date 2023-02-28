"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        self.input_file = input_file
        self.input_lines = input_file.read().splitlines()
        self.lines_quantity = len(self.input_lines)
        self.cur_line_idx = 0
        self.cur_command = self.input_lines[self.cur_line_idx].split("/", 1)[0].replace(" ", "")

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.cur_line_idx < self.lines_quantity

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        self.cur_line_idx += 1
        if self.has_more_commands():
            self.cur_command = self.input_lines[self.cur_line_idx].split("/", 1)[0].replace(" ", "")

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        # Your code goes here!
        if self.cur_command[0] == '@':
            return "A_COMMAND"
        if self.cur_command[0] == '(':
            return "L_COMMAND"
        return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or
            "L_COMMAND".
        """
        if self.command_type() == "L_COMMAND":
            return self.cur_command[1:len(self.cur_command)-1]
        if self.command_type() == "A_COMMAND":
            return self.cur_command[1:]

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        if "=" not in self.cur_command:
            return "null"
        return self.cur_command.split("=")[0]

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        dest_and_cmp = self.cur_command.split(";")[0].split("=")
        if len(dest_and_cmp) == 1:
            return dest_and_cmp[0]
        return dest_and_cmp[1]

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called
            only when commandType() is "C_COMMAND".
        """
        if ";" not in self.cur_command:
            return "null"
        return self.cur_command.split(";")[1]
