"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re

IDENTIFIER_REGEX = '\w+'
INTEGER_REGEX = '\d+'
STRING_REGEX = '\".*?\"'
KEYWORD_REGEX = ('class|method|function|constructor|int|boolean|char|void|'
                 'var|static|field|let|do|if|else|while|return|true|false|'
                 'null|this')
SYMBOL_REGEX = '{|}|\[|\]|\(|\)|\.|,|;|\+|-|\*|\/|&|\||<|>|=|~'
COMMENT_REGEX = '\/\*.*\*\/'


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    
    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters, 
    and comments, which are ignored. There are three possible comment formats: 
    /* comment until closing */ , /** API comment until closing */ , and 
    // comment until the line’s end.

    - ‘xxx’: quotes are used for tokens that appear verbatim (‘terminals’).
    - xxx: regular typeface is used for names of language constructs 
           (‘non-terminals’).
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate 
    file. A compilation unit is a single class. A class is a sequence of tokens 
    structured according to the following context free syntax:
    
    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) 
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement | 
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions
    
    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'
    
    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # A good place to start is to read all the lines of the input:
        input_lines = input_stream.read().splitlines()

        composed_regex = r'({}|{}|{}|{}|{})'.format(IDENTIFIER_REGEX,
                                                    INTEGER_REGEX,
                                                    STRING_REGEX,
                                                    KEYWORD_REGEX,
                                                    SYMBOL_REGEX)
        tokens = []
        self.is_comment_paragraph = False
        for line in input_lines:

            # remove comments:
            line = re.sub(COMMENT_REGEX, '', line)
            if line.strip()[0:2] == "/*":
                self.is_comment_paragraph = True
                continue
            if line.strip()[-2:] == '*/':
                self.is_comment_paragraph = False
                continue
            if self.is_comment_paragraph:
                continue

            line, strings_dict = JackTokenizer._replace_strings_with_temp_numbers(line)
            line = line.split("//")[0].lstrip()
            if not line:
                continue
            slice_line = re.findall(composed_regex, line)
            JackTokenizer._replace_numbers_with_original_strings(slice_line, strings_dict)
            tokens.extend(slice_line)
        self.tokens = tokens
        self.cur_line_idx = 0
        self.cur_token = self.tokens[self.cur_line_idx]
        self.tokens_num = len(tokens)

    @staticmethod
    def _replace_numbers_with_original_strings(slice_line, strings_dict):
        for j in range(len(slice_line)):
            if re.match(STRING_REGEX, slice_line[j]):
                slice_line[j] = strings_dict[int(slice_line[j].replace('"', ''))]

    @staticmethod
    def _replace_strings_with_temp_numbers(line):
        strings = re.findall(STRING_REGEX, line)
        strings_dict = {i: strings[i] for i in range(len(strings))}
        for i in strings_dict:
            line = line.replace(strings_dict[i], '"{}"'.format(i))
        return line, strings_dict

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        return self.cur_line_idx + 1 < self.tokens_num

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        self.cur_line_idx += 1
        self.cur_token = self.tokens[self.cur_line_idx]

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        if re.fullmatch(INTEGER_REGEX, self.cur_token):
            return "INT_CONST"
        if re.fullmatch(STRING_REGEX, self.cur_token):
            return "STRING_CONST"
        if re.fullmatch(KEYWORD_REGEX, self.cur_token):
            return "KEYWORD"
        if re.fullmatch(SYMBOL_REGEX, self.cur_token):
            return "SYMBOL"
        if re.fullmatch(IDENTIFIER_REGEX, self.cur_token):
            return "IDENTIFIER"

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        keyword_dict = {'class': "CLASS", 'method': "METHOD", 'function': "FUNCTION", 'constructor': "CONSTRUCTOR",
                        'int': "INT", 'boolean': "BOOLEAN", 'char': "CHAR", 'void': "VOID", 'var': "VAR",
                        'static': "STATIC", 'field': "FIELD", 'let': "LET", 'do': "DO", 'if': "IF", 'else': "ELSE",
                        'while': "WHILE", 'return': "RETURN", 'true': "TRUE", 'false': "FALSE", 'null': "NULL",
                        'this': "THIS"}
        return keyword_dict[self.cur_token]

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        return self.cur_token

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
            Recall that identifiers were defined in the grammar like so:
            identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
        """
        return self.cur_token

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        return int(self.cur_token)

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
        """
        return self.cur_token.replace('"', '')
