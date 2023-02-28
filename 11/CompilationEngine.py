"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

import JackTokenizer
import VMWriter
from SymbolTable import SymbolTable

UNARY_OP_DICT = {'-': "NEG", '~': "NOT", '^': "SHIFTLEFT", '#': "SHIFTRIGHT"}
BINARY_OP_DICT = {'+': "ADD", '-': "SUB", '*': "", '/': "", '&': "AND", '|': "OR", '<': "LT", '>': "GT", '=': "EQ"}
SEGMENT_DICT = {"STATIC": "STATIC", "FIELD": "THIS", "ARG": "ARG", "VAR": "LOCAL"}

class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: JackTokenizer, output_stream: VMWriter) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.symbol_table = SymbolTable()
        self.tokenizer = input_stream
        self.vm_writer = output_stream
        self.current_class = ''
        self.if_counter = 0
        self.while_counter = 0

    def _compile_type(self):
        if self.tokenizer.token_type() == "KEYWORD":
            _type = self.tokenizer.keyword()
        elif self.tokenizer.token_type() == "IDENTIFIER":
            _type = self.tokenizer.identifier()
        self.tokenizer.advance()
        return _type

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.symbol_table = SymbolTable()
        self.tokenizer.advance()
        self.current_class = self.tokenizer.identifier()
        self.tokenizer.advance()
        self.tokenizer.advance()
        self.compile_class_var_dec()
        while self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() in {"CONSTRUCTOR", "FUNCTION",
                                                                                        "METHOD"}:
            self.compile_subroutine()

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        while self.tokenizer.token_type() == "KEYWORD" and \
                (self.tokenizer.keyword() == "STATIC" or self.tokenizer.keyword() == "FIELD"):
            field_or_static = self.tokenizer.keyword()
            self.tokenizer.advance()  # field \ static
            _type = self._compile_type()
            name = self.tokenizer.identifier()
            self.symbol_table.define(name, _type, field_or_static)
            self.tokenizer.advance()  # name
            while self.tokenizer.symbol() != ";":
                self.tokenizer.advance()
                name = self.tokenizer.identifier()
                self.symbol_table.define(name, _type, field_or_static)
                self.tokenizer.advance()
            self.tokenizer.advance()

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.symbol_table.start_subroutine()
        subroutine_type = self.tokenizer.keyword()
        self.tokenizer.advance()  # subroutine_type (constructor / function / method)
        self.tokenizer.advance()  # return value

        if subroutine_type == "CONSTRUCTOR":
            func_name = self.current_class + "." + self.tokenizer.identifier()
            self.tokenizer.advance()  # new
            self.tokenizer.advance()  # (
            self.compile_parameter_list()
            self.tokenizer.advance()  # )
            self.tokenizer.advance()  # {
            self.compile_var_dec()
            self.vm_writer.write_function(func_name, self.symbol_table.var_count("VAR"))
            self.vm_writer.write_push("CONST", self.symbol_table.var_count("FIELD"))
            self.vm_writer.write_call("Memory.alloc", 1)
            self.vm_writer.write_pop("POINTER", 0)

        elif subroutine_type == "FUNCTION":
            func_name = self.current_class + "." + self.tokenizer.identifier()
            self.tokenizer.advance()   # name
            self.tokenizer.advance()   # (
            self.compile_parameter_list()
            self.tokenizer.advance()   # )
            self.tokenizer.advance()   # {
            self.compile_var_dec()
            self.vm_writer.write_function(func_name, self.symbol_table.var_count("VAR"))

        elif subroutine_type == "METHOD":
            method_name = self.tokenizer.identifier()
            self.tokenizer.advance()  # name
            self.tokenizer.advance()  # (
            self.symbol_table.define("this", self.current_class, "ARG")
            self.compile_parameter_list()
            self.tokenizer.advance()  # )
            self.tokenizer.advance()  # {
            self.compile_var_dec()
            self.vm_writer.write_function(self.current_class + "." + method_name, self.symbol_table.var_count("VAR"))
            self.vm_writer.write_push("ARG", 0)
            self.vm_writer.write_pop("POINTER", 0)

        self.compile_statements()
        self.tokenizer.advance()

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ')':
            return
        _type = self._compile_type()
        name = self.tokenizer.identifier()
        self.symbol_table.define(name, _type, "ARG")
        self.tokenizer.advance()   # name
        while self.tokenizer.symbol() != ")":
            self.tokenizer.advance()   # ,
            _type = self._compile_type()
            name = self.tokenizer.identifier()
            self.symbol_table.define(name, _type, "ARG")
            self.tokenizer.advance()  # name

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        while self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "VAR":
            self.tokenizer.advance()
            _type = self._compile_type()
            name = self.tokenizer.identifier()
            self.symbol_table.define(name, _type, "VAR")
            self.tokenizer.advance()
            while self.tokenizer.symbol() != ";":
                self.tokenizer.advance()
                name = self.tokenizer.identifier()
                self.symbol_table.define(name, _type, "VAR")
                self.tokenizer.advance()
            self.tokenizer.advance()

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        while self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() in {"IF", "LET", "DO", "WHILE",
                                                                                        "RETURN"}:
            if self.tokenizer.keyword() == "IF":
                self.compile_if()
            elif self.tokenizer.keyword() == "LET":
                self.compile_let()
            elif self.tokenizer.keyword() == "DO":
                self.compile_do()
            elif self.tokenizer.keyword() == "WHILE":
                self.compile_while()
            elif self.tokenizer.keyword() == "RETURN":
                self.compile_return()

    def _compile_subroutine_call(self):
        is_method = False
        first = self.tokenizer.identifier()
        self.tokenizer.advance()    # before .
        if self.tokenizer.symbol() == '(':
            is_method = True
            subroutine_name = self.current_class + "." + first
            self.vm_writer.write_push("POINTER", 0)
        elif self.tokenizer.symbol() == '.':
            if self.symbol_table.type_of(first):
                class_name = self.symbol_table.type_of(first)
                is_method = True
                segment = SEGMENT_DICT[self.symbol_table.kind_of(first)]
                self.vm_writer.write_push(segment, self.symbol_table.index_of(first))
            else:
                class_name = first
            self.tokenizer.advance()   # .
            subroutine_name = class_name + '.' + self.tokenizer.identifier()
            self.tokenizer.advance()   # after .
        self.tokenizer.advance()   # (
        arguments_num = self.compile_expression_list()
        if is_method:
            arguments_num += 1
        self.tokenizer.advance()   # )
        self.vm_writer.write_call(subroutine_name, arguments_num)

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.tokenizer.advance()   # do
        self._compile_subroutine_call()
        self.tokenizer.advance()
        self.vm_writer.write_pop("TEMP", 0)

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.tokenizer.advance()   # let
        var_name = self.tokenizer.identifier()
        self.tokenizer.advance()   # varName
        if self.tokenizer.symbol() == '[':
            self.tokenizer.advance()   # [
            segment = SEGMENT_DICT[self.symbol_table.kind_of(var_name)]
            self.vm_writer.write_push(segment, self.symbol_table.index_of(var_name))
            self.compile_expression()
            self.tokenizer.advance()    # ]
            self.vm_writer.write_arithmetic("ADD")
            self.tokenizer.advance()    # =
            self.compile_expression()
            self.vm_writer.write_pop("TEMP", 0)
            self.vm_writer.write_pop("POINTER", 1)
            self.vm_writer.write_push("TEMP", 0)
            self.vm_writer.write_pop("THAT", 0)
        else:
            self.tokenizer.advance()   # =
            self.compile_expression()
            segment = SEGMENT_DICT[self.symbol_table.kind_of(var_name)]
            self.vm_writer.write_pop(segment, self.symbol_table.index_of(var_name))
        self.tokenizer.advance()  # ;

    def compile_while(self) -> None:
        """Compiles a while statement."""
        while_idx = self.while_counter
        cond_label = f"while_condition.{while_idx}".upper()
        end_label = f"end_of_while_loop.{while_idx}".upper()
        self.while_counter += 1
        self.tokenizer.advance()
        self.tokenizer.advance()
        self.vm_writer.write_label(cond_label)
        self.compile_expression()
        self.tokenizer.advance()
        self.vm_writer.write_arithmetic("NOT")
        self.tokenizer.advance()
        self.vm_writer.write_if(end_label)
        self.compile_statements()
        self.vm_writer.write_goto(cond_label)
        self.vm_writer.write_label(end_label)
        self.tokenizer.advance()

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.tokenizer.advance()
        if (self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() != ';') \
                or self.tokenizer.token_type() != "SYMBOL":
            self.compile_expression()
        else:
            self.vm_writer.write_push("CONST", 0)
        self.vm_writer.write_return()
        self.tokenizer.advance()

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        if_idx = self.if_counter
        self.if_counter += 1
        if_false_label = f"IF_FALSE.{if_idx}"
        if_true_label = f"IF_TRUE.{if_idx}"
        end_if_label = f"END_IF.{if_idx}"
        self.tokenizer.advance()  # if
        self.tokenizer.advance()  # (
        self.compile_expression()
        self.tokenizer.advance()   # )
        self.tokenizer.advance()   # {
        self.vm_writer.write_if(if_true_label)
        self.vm_writer.write_goto(if_false_label)
        self.vm_writer.write_label(if_true_label)
        self.compile_statements()
        self.tokenizer.advance()   # }
        self.vm_writer.write_goto(end_if_label)
        self.vm_writer.write_label(if_false_label)
        if self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "ELSE":
            self.tokenizer.advance()    # else
            self.tokenizer.advance()    # {
            self.compile_statements()
            self.tokenizer.advance()    # }
        self.vm_writer.write_label(end_if_label)

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.compile_term()
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() in BINARY_OP_DICT:
            binary_op_symbol = self.tokenizer.symbol()
            self.tokenizer.advance()
            self.compile_term()
            if binary_op_symbol == '*':
                self.vm_writer.write_call('Math.multiply', 2)
            elif binary_op_symbol == '/':
                self.vm_writer.write_call('Math.divide', 2)
            else:
                self.vm_writer.write_arithmetic(BINARY_OP_DICT[binary_op_symbol])

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        if self.tokenizer.token_type() == "INT_CONST":
            self.vm_writer.write_push("CONST", self.tokenizer.int_val())
            self.tokenizer.advance()

        elif self.tokenizer.token_type() == "STRING_CONST":
            string = self.tokenizer.string_val()
            length = len(string)
            self.vm_writer.write_push("CONST", length)
            self.vm_writer.write_call("String.new", 1)
            for letter in string:
                self.vm_writer.write_push("CONST", ord(letter))
                self.vm_writer.write_call("String.appendChar", 2)
            self.tokenizer.advance()

        elif self.tokenizer.token_type() == "KEYWORD":
            if self.tokenizer.keyword() == "FA LSE":
                self.vm_writer.write_push("CONST", 0)

            elif self.tokenizer.keyword() == "TRUE":
                self.vm_writer.write_push("CONST", 1)
                self.vm_writer.write_arithmetic("NEG")

            elif self.tokenizer.keyword() == "NULL":
                self.vm_writer.write_push("CONST", 0)

            elif self.tokenizer.keyword() == "THIS":
                self.vm_writer.write_push("POINTER", 0)

            self.tokenizer.advance()

        elif self.tokenizer.token_type() == "SYMBOL":

            if self.tokenizer.symbol() == '(':    # (expression)
                self.tokenizer.advance()
                self.compile_expression()
                self.tokenizer.advance()

            elif self.tokenizer.symbol() in UNARY_OP_DICT:   # unary_op term
                unary_op_symbol = self.tokenizer.symbol()
                self.tokenizer.advance()
                self.compile_term()
                self.vm_writer.write_arithmetic(UNARY_OP_DICT[unary_op_symbol])

        elif self.tokenizer.token_type() == "IDENTIFIER":
            identifier = self.tokenizer.identifier()
            self.tokenizer.advance()
            if self.tokenizer.token_type() == "SYMBOL":
                if self.tokenizer.symbol() == '[':      # varName[expression]
                    self.tokenizer.advance()   # [
                    segment = SEGMENT_DICT[self.symbol_table.kind_of(identifier)]
                    self.vm_writer.write_push(segment, self.symbol_table.index_of(identifier))
                    self.compile_expression()
                    self.vm_writer.write_arithmetic("ADD")
                    self.vm_writer.write_pop("POINTER", 1)
                    self.vm_writer.write_push("THAT", 0)
                    self.tokenizer.advance()   # ]

                elif self.tokenizer.symbol() in {'(', '.'}:
                    is_method = False
                    if self.tokenizer.symbol() == '(':    # subroutine_name(expression_list)
                        subroutine_name = identifier
                        is_method = True
                    elif self.tokenizer.symbol() == '.':   # ( class_name | var_name ) . subroutine_name (
                        class_or_var_name = identifier
                        kind_of_var_name = self.symbol_table.kind_of(class_or_var_name)
                        if kind_of_var_name:    # not null, exist in symbol table
                            is_method = True
                            self.vm_writer.write_push(SEGMENT_DICT[kind_of_var_name], self.symbol_table.index_of(class_or_var_name))
                            class_or_var_name = self.symbol_table.type_of(class_or_var_name)
                        self.tokenizer.advance()
                        subroutine_name = class_or_var_name + '.' + self.tokenizer.identifier()
                        self.tokenizer.advance()
                    self.tokenizer.advance()
                    arguments_num = self.compile_expression_list()
                    if is_method:
                        arguments_num += 1
                    self.tokenizer.advance()
                    self.vm_writer.write_call(subroutine_name, arguments_num)

                else:    # varName
                    segment = SEGMENT_DICT[self.symbol_table.kind_of(identifier)]
                    self.vm_writer.write_push(segment, self.symbol_table.index_of(identifier))

    def compile_expression_list(self) -> int:
        arguments_num = 0
        if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ")":
            return arguments_num
        self.compile_expression()
        arguments_num = 1
        while self.tokenizer.symbol() == ',':
            self.tokenizer.advance()
            self.compile_expression()
            arguments_num += 1
        return arguments_num
