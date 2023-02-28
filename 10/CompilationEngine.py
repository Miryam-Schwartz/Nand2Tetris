"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

import JackTokenizer


def _is_op(symbol: str):
    return symbol in {'+', '-', '*', '/', '&', '|', '<', '>', '='}


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: JackTokenizer, output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.tokenizer = input_stream
        self.output_stream = output_stream

    def _compile_symbol(self):
        symbol = self.tokenizer.symbol()
        symbol_dict = {'<': '&lt;', '>': '&gt;', '&': '&amp;'}
        if symbol in symbol_dict:
            symbol = symbol_dict[symbol]
        self.output_stream.write("<symbol> " + symbol + " </symbol>\n")
        self.tokenizer.advance()

    def _compile_identifier(self):
        self.output_stream.write("<identifier> " + self.tokenizer.identifier() + " </identifier>\n")
        self.tokenizer.advance()

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.output_stream.write("<class>\n")
        self.output_stream.write("<keyword> class </keyword>\n")
        self.tokenizer.advance()
        self._compile_identifier()
        self._compile_symbol()
        self.compile_class_var_dec()
        while self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() in {"CONSTRUCTOR", "FUNCTION", "METHOD"}:
            self.compile_subroutine()
        self.output_stream.write("<symbol> " + self.tokenizer.symbol() + " </symbol>\n")
        self.output_stream.write("</class>\n")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        while self.tokenizer.token_type() == "KEYWORD" and\
                (self.tokenizer.keyword() == "STATIC" or self.tokenizer.keyword() == "FIELD"):
            self.output_stream.write("<classVarDec>\n")
            if self.tokenizer.keyword() == "STATIC":
                self.output_stream.write("<keyword> static </keyword>\n")
            elif self.tokenizer.keyword() == "FIELD":
                self.output_stream.write("<keyword> field </keyword>\n")
            self.tokenizer.advance()
            self._compile_type()
            self._compile_identifier()
            while self.tokenizer.symbol() != ";":
                self._compile_symbol()
                self._compile_identifier()
            self._compile_symbol()
            self.output_stream.write("</classVarDec>\n")

    def _compile_type(self):
        if self.tokenizer.token_type() == "KEYWORD":
            if self.tokenizer.keyword() == "VOID":
                self.output_stream.write("<keyword> void </keyword>\n")
            elif self.tokenizer.keyword() == "CHAR":
                self.output_stream.write("<keyword> char </keyword>\n")
            elif self.tokenizer.keyword() == "INT":
                self.output_stream.write("<keyword> int </keyword>\n")
            elif self.tokenizer.keyword() == "BOOLEAN":
                self.output_stream.write("<keyword> boolean </keyword>\n")
        else:
            self.output_stream.write("<identifier> " + self.tokenizer.identifier() + " </identifier>\n")
        self.tokenizer.advance()

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.output_stream.write("<subroutineDec>\n")
        if self.tokenizer.keyword() == "CONSTRUCTOR":
            self.output_stream.write("<keyword> constructor </keyword>\n")
        elif self.tokenizer.keyword() == "FUNCTION":
            self.output_stream.write("<keyword> function </keyword>\n")
        elif self.tokenizer.keyword() == "METHOD":
            self.output_stream.write("<keyword> method </keyword>\n")
        self.tokenizer.advance()
        self._compile_type()
        self._compile_identifier()
        self._compile_symbol()
        self.compile_parameter_list()
        self._compile_symbol()
        self.output_stream.write("<subroutineBody>\n")
        self._compile_symbol()
        self.compile_var_dec()
        self.compile_statements()
        self._compile_symbol()
        self.output_stream.write("</subroutineBody>\n")
        self.output_stream.write("</subroutineDec>\n")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        self.output_stream.write("<parameterList>\n")
        if self.tokenizer.token_type() != "SYMBOL":
            self._compile_type()
            self._compile_identifier()
        while self.tokenizer.symbol() != ")":
            self._compile_symbol()
            self._compile_type()
            self._compile_identifier()
        self.output_stream.write("</parameterList>\n")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        while self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "VAR":
            self.output_stream.write("<varDec>\n")
            self.output_stream.write("<keyword> var </keyword>\n")
            self.tokenizer.advance()
            self._compile_type()
            self._compile_identifier()
            while self.tokenizer.symbol() != ";":
                self._compile_symbol()
                self._compile_identifier()
            self._compile_symbol()
            self.output_stream.write("</varDec>\n")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        self.output_stream.write("<statements>\n")
        while self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() in {"IF", "LET", "DO", "WHILE", "RETURN"}:
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
        self.output_stream.write("</statements>\n")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.output_stream.write("<doStatement>\n")
        self.output_stream.write("<keyword> do </keyword>\n")
        self.tokenizer.advance()
        self._compile_identifier()
        if self.tokenizer.symbol() == ".":
            self._compile_symbol()
            self._compile_identifier()
        self._compile_symbol()
        self.compile_expression_list()
        self._compile_symbol()

        self._compile_symbol()

        self.output_stream.write("</doStatement>\n")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.output_stream.write("<letStatement>\n")
        self.output_stream.write("<keyword> let </keyword>\n")
        self.tokenizer.advance()
        self._compile_identifier()
        if self.tokenizer.symbol() == "[":
            self._compile_symbol()
            self.compile_expression()
            self._compile_symbol()
        self._compile_symbol()
        self.compile_expression()
        self._compile_symbol()
        self.output_stream.write("</letStatement>\n")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.output_stream.write("<whileStatement>\n")
        self.output_stream.write("<keyword> while </keyword>\n")
        self.tokenizer.advance()
        self._compile_symbol()
        self.compile_expression()
        self._compile_symbol()
        self._compile_symbol()
        self.compile_statements()
        self._compile_symbol()
        self.output_stream.write("</whileStatement>\n")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.output_stream.write("<returnStatement>\n")
        self.output_stream.write("<keyword> return </keyword>\n")
        self.tokenizer.advance()
        if (self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() != ';')\
                or self.tokenizer.token_type() != "SYMBOL":
            self.compile_expression()
        self._compile_symbol()
        self.output_stream.write("</returnStatement>\n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.output_stream.write("<ifStatement>\n")
        self.output_stream.write("<keyword> if </keyword>\n")
        self.tokenizer.advance()
        self._compile_symbol()
        self.compile_expression()
        self._compile_symbol()
        self._compile_symbol()
        self.compile_statements()
        self._compile_symbol()
        if self.tokenizer.token_type() == "KEYWORD":
            if self.tokenizer.keyword() == "ELSE":
                self.output_stream.write("<keyword> else </keyword>\n")
                self.tokenizer.advance()
                self._compile_symbol()
                self.compile_statements()
                self._compile_symbol()
        self.output_stream.write("</ifStatement>\n")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self.output_stream.write("<expression>\n")
        self.compile_term()
        while self.tokenizer.token_type() == "SYMBOL" and _is_op(self.tokenizer.symbol()):
            self._compile_symbol()
            self.compile_term()
        self.output_stream.write("</expression>\n")

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
        self.output_stream.write("<term>\n")
        if self.tokenizer.token_type() == "INT_CONST":
            self.output_stream.write("<integerConstant> " + str(self.tokenizer.int_val()) + " </integerConstant>\n")
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == "STRING_CONST":
            self.output_stream.write("<stringConstant> " + self.tokenizer.string_val() + " </stringConstant>\n")
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == "KEYWORD":
            self.output_stream.write("<keyword> " + self.tokenizer.keyword().lower() + " </keyword>\n")
            self.tokenizer.advance()

        elif self.tokenizer.token_type() == "SYMBOL":
            if self.tokenizer.symbol() == '(':
                self._compile_symbol()
                self.compile_expression()
                self._compile_symbol()
            elif self.tokenizer.symbol() in {'-', '~', '^', '#'}:
                self._compile_symbol()
                self.compile_term()

        elif self.tokenizer.token_type() == "IDENTIFIER":
            self._compile_identifier()
            if self.tokenizer.token_type() == "SYMBOL":
                if self.tokenizer.symbol() == '[':
                    self._compile_symbol()
                    self.compile_expression()
                    self._compile_symbol()
                elif self.tokenizer.symbol() == '(':
                    self._compile_symbol()
                    self.compile_expression_list()
                    self._compile_symbol()
                elif self.tokenizer.symbol() == '.':
                    self._compile_symbol()
                    self._compile_identifier()
                    self._compile_symbol()
                    self.compile_expression_list()
                    self._compile_symbol()
        self.output_stream.write("</term>\n")

    def compile_expression_list(self) -> None:
        self.output_stream.write("<expressionList>\n")
        if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ")":
            self.output_stream.write("</expressionList>\n")
            return
        self.compile_expression()
        while self.tokenizer.symbol() == ',':
            self._compile_symbol()
            self.compile_expression()
        self.output_stream.write("</expressionList>\n")
