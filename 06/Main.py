"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """

    parser = Parser(input_file)
    symbolTable = SymbolTable()

    # first pass
    cmd_num = 0
    while parser.has_more_commands():
        if parser.cur_command == '' or parser.cur_command[0] == '/':
            parser.advance()
            continue
        if parser.command_type() == "A_COMMAND" or parser.command_type() == "C_COMMAND":
            cmd_num += 1
            parser.advance()
            continue
        elif parser.command_type() == "L_COMMAND":
            if not symbolTable.contains(parser.symbol()):
                symbolTable.add_entry(parser.symbol(), cmd_num)
            parser.advance()

    # second pass
    input_file.seek(0)
    parser = Parser(input_file)
    ram_counter = 16

    while parser.has_more_commands():
        if parser.cur_command == '' or parser.cur_command[0] == '/':
            parser.advance()
            continue
        if parser.cur_command == "L_COMMAND":
            parser.advance()
            continue
        if parser.command_type() == "A_COMMAND":
            if parser.symbol().isnumeric():
                numeric_val = int(parser.symbol())
            elif symbolTable.contains(parser.symbol()):
                numeric_val = symbolTable.get_address(parser.symbol())
            else:
                symbolTable.add_entry(parser.symbol(), ram_counter)
                numeric_val = ram_counter
                ram_counter += 1
            binary_cmd = bin(numeric_val)[2:]
            length = len(binary_cmd)
            output_file.write((16 - length) * '0' + binary_cmd + '\n')
        elif parser.command_type() == "C_COMMAND":
            if '<' in parser.comp() or '>' in parser.comp():
                output_file.write(Code.comp(parser.comp()) + Code.dest(parser.dest()) + Code.jump(parser.jump()) + '\n')
            else:
                output_file.write(3 * '1' + Code.comp(parser.comp()) + Code.dest(parser.dest()) + Code.jump(parser.jump()) + '\n')
        parser.advance()


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
