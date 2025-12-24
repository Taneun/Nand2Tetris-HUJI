"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        self.tokenizer = input_stream
        self.output_stream = output_stream
        self.indent_level = 0  # Helps manage XML indentation

    def write_line(self, line: str) -> None:
        """
        Writes an indented line to the output stream.
        Note: This advances the tokenizer!
        """
        self.output_stream.write("  " * self.indent_level + line + "\n")
        self.tokenizer.advance()

    def write_keyword(self, keyword: str) -> None:
        """Writes a keyword to the output stream."""
        self.write_line(f"<keyword> {keyword.lower()} </keyword>")

    def write_symbol(self, symbol: str) -> None:
        """Writes a symbol to the output stream."""
        self.write_line(f"<symbol> {symbol} </symbol>")

    def write_identifier(self, identifier: str) -> None:
        """Writes an identifier to the output stream."""
        self.write_line(f"<identifier> {identifier} </identifier>")

    def write_opening_tag(self, tag: str) -> None:
        """Writes an opening XML tag."""
        self.output_stream.write("  " * self.indent_level + f"<{tag}>" + "\n")
        self.indent_level += 1

    def write_closing_tag(self, tag: str) -> None:
        """Writes a closing XML tag."""
        self.indent_level -= 1
        self.output_stream.write("  " * self.indent_level + f"</{tag}>" + "\n")

    def compile_class(self) -> None:
        """Compiles a complete class: 'class' className '{' classVarDec* subroutineDec* '}'"""
        self.write_opening_tag("class")
        # 'class'
        self.write_keyword(self.tokenizer.keyword())
        # className
        self.write_identifier(self.tokenizer.identifier())
        # '{'
        self.write_symbol(self.tokenizer.symbol())

        while self.tokenizer.has_more_tokens():
            if self.tokenizer.keyword() in ("STATIC", "FIELD"):
                self.compile_class_var_dec()
            # subroutineDec*
            elif self.tokenizer.keyword() in ("CONSTRUCTOR", "FUNCTION", "METHOD"):
                self.compile_subroutine()
            elif self.tokenizer.symbol() == "}":
                break

        # '}'
        self.write_symbol(self.tokenizer.symbol())
        self.write_closing_tag("class")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration: ('static' | 'field') type varName (',' varName)* ';'"""
        self.write_opening_tag("classVarDec")
        # 'static' | 'field'
        self.write_keyword(self.tokenizer.keyword())
        # type
        if self.tokenizer.token_type() == "KEYWORD":
            self.write_keyword(self.tokenizer.keyword())
        else:
            self.write_identifier(self.tokenizer.identifier())
        # varName
        while True:
            self.write_identifier(self.tokenizer.identifier())
            # ',' or ';'
            if self.tokenizer.symbol() == ";":
                self.write_symbol(self.tokenizer.symbol())
                break
            self.write_symbol(self.tokenizer.symbol())
        self.write_closing_tag("classVarDec")

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.write_opening_tag("subroutineDec")
        # 'constructor' | 'function' | 'method'
        self.write_keyword(self.tokenizer.keyword())
        # 'void' | type
        if self.tokenizer.token_type() == "KEYWORD":
            self.write_keyword(self.tokenizer.keyword())
        else:
            self.write_identifier(self.tokenizer.identifier())
        # subroutineName
        self.write_identifier(self.tokenizer.identifier())
        # '(' parameterList ')'
        self.write_symbol(self.tokenizer.symbol())
        self.compile_parameter_list()
        self.write_symbol(self.tokenizer.symbol())
        # subroutineBody
        self.write_opening_tag("subroutineBody")
        self.write_symbol(self.tokenizer.symbol())
        while self.tokenizer.keyword() == "VAR":
            self.compile_var_dec()
        self.compile_statements()
        self.write_symbol(self.tokenizer.symbol())
        self.write_closing_tag("subroutineBody")
        self.write_closing_tag("subroutineDec")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        self.write_opening_tag("parameterList")
        # Check if there is at least one parameter (type varName)
        if self.tokenizer.token_type() in ("KEYWORD", "IDENTIFIER"):
            # First parameter (type varName)
            if self.tokenizer.token_type() == "KEYWORD":
                self.write_keyword(self.tokenizer.keyword())  # Type
            else:
                self.write_identifier(self.tokenizer.identifier())  # Type
            self.write_identifier(self.tokenizer.identifier())  # varName
            # Handle additional parameters (', type varName')
            while self.tokenizer.symbol() == ",":
                self.write_symbol(self.tokenizer.symbol())  # ','
                # Type
                if self.tokenizer.token_type() == "KEYWORD":
                    self.write_keyword(self.tokenizer.keyword())
                else:
                    self.write_identifier(self.tokenizer.identifier())
                # varName
                self.write_identifier(self.tokenizer.identifier())
        self.write_closing_tag("parameterList")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration: 'var' type varName (',' varName)* ';'"""
        self.write_opening_tag("varDec")
        # 'var'
        self.write_keyword(self.tokenizer.keyword())
        # type
        if self.tokenizer.token_type() == "KEYWORD":
            self.write_keyword(self.tokenizer.keyword())
        else:
            self.write_identifier(self.tokenizer.identifier())
        # varName
        while True:
            self.write_identifier(self.tokenizer.identifier())
            # ',' or ';'
            if self.tokenizer.symbol() == ";":
                self.write_symbol(self.tokenizer.symbol())
                break
            self.write_symbol(self.tokenizer.symbol())
        self.write_closing_tag("varDec")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        compile_functions = {
            "LET": self.compile_let,
            "IF": self.compile_if,
            "WHILE": self.compile_while,
            "DO": self.compile_do,
            "RETURN": self.compile_return
        }
        self.write_opening_tag("statements")
        while self.tokenizer.has_more_tokens() and self.tokenizer.token_type() != "SYMBOL":
            compile_functions[self.tokenizer.keyword()]()
        self.write_closing_tag("statements")

    def compile_do(self) -> None:
        """Compiles a do statement: doStatement: 'do' subroutineCall ';'"""
        self.write_opening_tag("doStatement")
        self.write_keyword(self.tokenizer.keyword())
        self.compile_subroutine_call()
        self.write_symbol(self.tokenizer.symbol())
        self.write_closing_tag("doStatement")

    def compile_let(self) -> None:
        """Compiles a let statement: letStatement: 'let' varName ('[' expression ']')? '=' expression ';'"""
        self.write_opening_tag("letStatement")
        self.write_keyword(self.tokenizer.keyword())
        self.write_identifier(self.tokenizer.identifier())
        if self.tokenizer.symbol() == "[":
            self.write_symbol(self.tokenizer.symbol())
            self.compile_expression()
            self.write_symbol(self.tokenizer.symbol())
        self.write_symbol(self.tokenizer.symbol())
        self.compile_expression()
        self.write_symbol(self.tokenizer.symbol())
        self.write_closing_tag("letStatement")

    def compile_while(self) -> None:
        """Compiles a while statement: 'while' '(' 'expression' ')' '{' statements '}'"""
        self.write_opening_tag("whileStatement")
        # 'while'
        self.write_keyword(self.tokenizer.keyword())
        # '('
        self.write_symbol(self.tokenizer.symbol())
        self.compile_expression()
        # ')'
        self.write_symbol(self.tokenizer.symbol())
        # '{'
        self.write_symbol(self.tokenizer.symbol())
        self.compile_statements()
        # '}'
        self.write_symbol(self.tokenizer.symbol())
        self.write_closing_tag("whileStatement")

    def compile_return(self) -> None:
        """Compiles a return statement: 'return' expression? ';'"""
        self.write_opening_tag("returnStatement")
        # 'return'
        self.write_keyword(self.tokenizer.keyword())
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ";":
            self.compile_expression()
        self.write_symbol(self.tokenizer.symbol())
        self.write_closing_tag("returnStatement")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else 
        clause: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?"""
        self.write_opening_tag("ifStatement")
        # 'if'
        self.write_keyword(self.tokenizer.keyword())
        # '('
        self.write_symbol(self.tokenizer.symbol())
        self.compile_expression()
        # ')'
        self.write_symbol(self.tokenizer.symbol())
        # '{'
        self.write_symbol(self.tokenizer.symbol())
        self.compile_statements()
        # '}'
        self.write_symbol(self.tokenizer.symbol())
        if self.tokenizer.keyword() == "ELSE":
            # 'else'
            self.write_keyword(self.tokenizer.keyword())
            # '{'
            self.write_symbol(self.tokenizer.symbol())
            self.compile_statements()
            # '}'
            self.write_symbol(self.tokenizer.symbol())
        self.write_closing_tag("ifStatement")

    def compile_expression(self) -> None:
        """Compiles an expression:
            - expression: term (op term)*
            - term: integerConstant | stringConstant | keywordConstant | varName |
                    varName '['expression']' | subroutineCall | '(' expression ')' |
                    unaryOp term
            - subroutineCall: subroutineName '(' expressionList ')' | (className |
                              varName) '.' subroutineName '(' expressionList ')'
            - expressionList: (expression (',' expression)* )?
            - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
            - unaryOp: '-' | '~' | '^' | '#'
            - keywordConstant: 'true' | 'false' | 'null' | 'this'"""
        self.write_opening_tag("expression")
        # Compile the first term
        self.compile_term()
        # Check and compile (op term)*
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() in \
                {"+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "="}: #todo here
            self.write_symbol(self.tokenizer.symbol())  # Write the operator
            self.compile_term()  # Compile the next term
        self.write_closing_tag("expression")

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
        self.write_opening_tag("term")
        token_type = self.tokenizer.token_type()
        if token_type == "INT_CONST":
            # Integer constant
            self.write_line(f"<integerConstant> {self.tokenizer.int_val()} </integerConstant>")
        elif token_type == "STRING_CONST":
            # String constant
            self.write_line(f"<stringConstant> {self.tokenizer.string_val()} </stringConstant>")
        elif token_type == "KEYWORD":
            # Keyword constant
            self.write_keyword(self.tokenizer.keyword())
        elif token_type == "SYMBOL":
            if self.tokenizer.symbol() == "(":
                # '(' expression ')'
                self.write_symbol(self.tokenizer.symbol())
                self.compile_expression()
                self.write_symbol(self.tokenizer.symbol())
            elif self.tokenizer.symbol() in {"-", "~", "^", "#"}: #todo here
                self.write_symbol(self.tokenizer.symbol())
                self.compile_term()
        elif token_type == "IDENTIFIER":
            # Lookahead to distinguish between varName, array, and subroutineCall
            identifier = self.tokenizer.identifier()
            self.tokenizer.advance()
            if self.tokenizer.symbol() == "[":
                # varName '[' expression ']'
                self.output_stream.write("  " * self.indent_level + f"<identifier> {identifier} </identifier>" + "\n")
                self.write_symbol(self.tokenizer.symbol())
                self.compile_expression()
                self.write_symbol(self.tokenizer.symbol())
            elif self.tokenizer.symbol() in {"(", "."}:
                # subroutineCall
                self.compile_subroutine_call(identifier)
            else:
                # Plain varName
                self.output_stream.write("  " * self.indent_level + f"<identifier> {identifier} </identifier>" + "\n")
        self.write_closing_tag("term")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.write_opening_tag("expressionList")
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ")":
            # There is at least one expression
            self.compile_expression()
            while self.tokenizer.symbol() == ",":
                self.write_symbol(self.tokenizer.symbol())  # Write ','
                self.compile_expression()
        self.write_closing_tag("expressionList")

    def compile_subroutine_call(self, sub_identifier=None) -> None:
        """Compiles a subroutine call:
        - subroutineName '(' expressionList ')'
        - (className | varName) '.' subroutineName '(' expressionList ')'
        """
        # subroutineName or (className | varName)
        if sub_identifier is None:
            # sub_identifier = self.tokenizer.identifier()
            self.write_identifier(self.tokenizer.identifier())
        else:
            self.output_stream.write("  " * self.indent_level + f"<identifier> {sub_identifier} </identifier>" + "\n")
        if self.tokenizer.symbol() == ".":
            # '.' indicates (className | varName) '.' subroutineName
            self.write_symbol(self.tokenizer.symbol())  # Write '.'
            self.write_identifier(self.tokenizer.identifier())  # subroutineName
        # '(' expressionList ')'
        self.write_symbol(self.tokenizer.symbol())  # Write '('
        self.compile_expression_list()  # Compile the expression list
        self.write_symbol(self.tokenizer.symbol())  # Write ')'
