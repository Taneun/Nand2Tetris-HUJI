"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import tokenize
from io import StringIO
import re


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
    TOKEN_TYPES = {
        "KEYWORD": ['class', 'constructor', 'function', 'method', 'field',
                    'static', 'var', 'int', 'char', 'boolean', 'void', 'true',
                    'false', 'null', 'this', 'let', 'do', 'if', 'else',
                    'while', 'return'],
        "SYMBOL": ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
                   '-', '*', '/', '&', '|', '<', '>', '=', '~', '^', '#']
    }

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        flat_code_str = self.remove_comments(input_stream)
        self.tokens = self.my_tokenize(flat_code_str)
        self.current_token_index = 0
        self.curr_token = self.tokens[0]

    def remove_comments(self, input_stream):
        input_lines = input_stream.read()

        def protect_strings(text):
            # Only match actual string literals that start with a quote
            # Must be preceded by start of line, space, or certain characters
            pattern = r'(?:^|[\s=+(,])("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')'
            strings = []

            def replace(match):
                # Only capture the string part, not the preceding character
                matched_str = match.group(1)
                strings.append(matched_str)
                return match.group(0)[0] + f"<STR_{len(strings) - 1}>"

            protected_text = re.sub(pattern, replace, text)
            return protected_text, strings

        def restore_strings(text, strings):
            for i, string in enumerate(strings):
                text = text.replace(f"<STR_{i}>", string)
            return text

        def remove_multiline_comments(text):
            # More robust pattern for multi-line comments
            # Using re.DOTALL to make . match newlines
            return re.sub(r'/\*[\s\S]*?\*/', '', text)

        def remove_singleline_comments(text):
            # Process line by line for single-line comments
            lines = []
            for line in text.splitlines():
                # Remove // comments
                line = re.sub(r'//.*$', '', line)
                if line.strip():
                    lines.append(line.strip())
            return '\n'.join(lines)

        # First protect strings
        protected_text, strings = protect_strings(input_lines)

        # Remove comments
        without_comments = remove_singleline_comments(protected_text)
        without_multiline = remove_multiline_comments(without_comments)

        # Restore strings and format
        final_result = restore_strings(without_multiline, strings)
        return ' '.join(line.strip() for line in final_result.splitlines() if line.strip())

    def my_tokenize(self, input_code: str) -> list[tuple[str, str]]:
        """
        Tokenizes the Jack code using custom parsing to fit Jack grammar.
        """
        result = []

        # Define regex for Jack tokens
        token_pattern = r"""
            ".*?"               |
            [\{\}\(\)\[\]\.,;\+\-\*/&|<>=~\^#] |
            \d+                 |
            [a-zA-Z_]\w*
        """
        token_regex = re.compile(token_pattern, re.VERBOSE)

        # Find all tokens
        tokens = token_regex.findall(input_code)

        for tokval in tokens:
            tokval = tokval.strip()
            if tokval == "":
                continue

            # Match Jack-specific token types
            if tokval in self.TOKEN_TYPES["KEYWORD"]:
                result.append(("KEYWORD", tokval))
            elif tokval in self.TOKEN_TYPES["SYMBOL"]:
                result.append(("SYMBOL", tokval))
            elif tokval.isdigit() and 0 <= int(tokval) <= 32767:
                result.append(("INT_CONST", tokval))
            elif tokval.startswith('"') and tokval.endswith('"'):
                result.append(("STRING_CONST", tokval[1:-1]))  # Remove quotes
            elif tokval[0].isalpha() or tokval[0] == "_":
                result.append(("IDENTIFIER", tokval))
            else:
                raise ValueError(f"Invalid token: {tokval}")

        return result

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        return self.current_token_index < len(self.tokens)

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        self.current_token_index += 1
        if self.has_more_tokens():
            self.curr_token = self.tokens[self.current_token_index]

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        return self.curr_token[0]

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        return self.curr_token[1].upper()

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        return self.curr_token[1]

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
        return self.curr_token[1]

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        return int(self.curr_token[1])

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
        """
        return self.curr_token[1]
