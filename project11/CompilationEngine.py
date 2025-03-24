"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unsupported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import JackTokenizer
import SymbolTable
import VMWriter


class CompilationEngine:
    VARS_MAP = {
        "ARG": "ARG",
        "VAR": "LOCAL",
        "STATIC": "STATIC",
        "FIELD": "THIS"
    }
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: JackTokenizer, vm_writer: VMWriter, symbol_table: SymbolTable) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        """
        self.symbol_table = symbol_table
        self.tokenizer = input_stream
        self.vm_writer = vm_writer
        self.class_name = None
        self.subroutine_name = None

    def compile_class(self) -> None:
        """Compiles a complete class: 'class' className '{' classVarDec* subroutineDec* '}'"""
        self.tokenizer.advance()  # 'class'
        self.class_name = self.tokenizer.identifier()
        self.tokenizer.advance()  # className
        self.tokenizer.advance()  # '{'

        while self.tokenizer.keyword() in ("STATIC", "FIELD"):
            self.compile_class_var_dec()

        while self.tokenizer.keyword() in ("CONSTRUCTOR", "FUNCTION", "METHOD"):
            self.compile_subroutine()
        self.tokenizer.advance()  # '}'

    def get_var_type(self) -> str:
        if self.tokenizer.token_type() == "KEYWORD":
            return self.tokenizer.keyword()
        return self.tokenizer.identifier()

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration: ('static' | 'field') type varName (',' varName)* ';'"""
        # 'static' | 'field'
        kind_ = self.tokenizer.keyword()
        self.tokenizer.advance()
        type_ = self.get_var_type()
        self.tokenizer.advance()
        name_ = self.tokenizer.identifier()
        self.tokenizer.advance()
        self.symbol_table.define(name_, type_, kind_)
        while self.tokenizer.symbol() == ",":
            self.tokenizer.advance()
            name_ = self.tokenizer.identifier()
            self.symbol_table.define(name_, type_, kind_)
            self.tokenizer.advance()
        self.tokenizer.advance()  # ';'

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """

        function_type = self.tokenizer.keyword()
        self.tokenizer.advance()  # 'constructor' | 'function' | 'method'
        self.tokenizer.advance()  # 'void' | type
        # subroutineName
        self.subroutine_name = self.class_name + "." + self.tokenizer.identifier()
        self.symbol_table.start_subroutine()
        self.tokenizer.advance()  # subroutineName
        if function_type == "METHOD":
            self.symbol_table.define("this", "self", "ARG")
        # '(' parameterList ')'
        self.tokenizer.advance()  # '('
        self.compile_parameter_list()
        self.tokenizer.advance()  # ')'
        # subroutineBody
        self.tokenizer.advance()  # '{'
        while self.tokenizer.keyword() == "VAR":
            self.compile_var_dec()
        num_vars = self.symbol_table.var_count("VAR")
        self.vm_writer.write_function(self.subroutine_name, num_vars)
        self.set_ptr(function_type)
        self.compile_statements()
        self.tokenizer.advance()  # '}'

    def set_ptr(self, function_type: str) -> None:
        if function_type == "METHOD":
            self.vm_writer.write_push("ARG", 0)
            self.vm_writer.write_pop("POINTER", 0)
        elif function_type == "CONSTRUCTOR":
            num_fields = self.symbol_table.var_count("FIELD")
            self.vm_writer.write_push("CONST", num_fields)
            self.vm_writer.write_call("Memory.alloc", 1)
            self.vm_writer.write_pop("POINTER", 0)

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Check if there is at least one parameter (type varName)
        if self.tokenizer.token_type() in ("KEYWORD", "IDENTIFIER"):
            # First parameter (type varName)
            type_ = self.get_var_type()
            self.tokenizer.advance()
            name_ = self.tokenizer.identifier()  # varName
            self.tokenizer.advance()
            self.symbol_table.define(name_, type_, "ARG")
            # Handle additional parameters (', type varName')
            while self.tokenizer.symbol() == ",":
                self.tokenizer.advance()  # ','
                type_ = self.get_var_type()
                self.tokenizer.advance()
                name_ = self.tokenizer.identifier()  # varName
                self.tokenizer.advance()
                self.symbol_table.define(name_, type_, "ARG")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration: 'var' type varName (',' varName)* ';'"""
        # 'var'
        kind_ = self.tokenizer.keyword()
        self.tokenizer.advance()
        # type
        type_ = self.get_var_type()
        self.tokenizer.advance()
        # varName
        name_ = self.tokenizer.identifier()
        self.tokenizer.advance()
        self.symbol_table.define(name_, type_, kind_)
        while self.tokenizer.symbol() == ",":
            self.tokenizer.advance()
            name_ = self.tokenizer.identifier()
            self.tokenizer.advance()
            self.symbol_table.define(name_, type_, kind_)
        self.tokenizer.advance()  # ';'

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
        while self.tokenizer.has_more_tokens() and self.tokenizer.token_type() != "SYMBOL":
            # Call the appropriate compile function, it advances the tokenizer
            compile_functions[self.tokenizer.keyword()]()

    def compile_do(self) -> None:
        """Compiles a do statement: doStatement: 'do' subroutineCall ';'"""
        self.tokenizer.advance()  # 'do'
        self.compile_subroutine_call()
        self.vm_writer.write_pop("TEMP", 0)
        self.tokenizer.advance()  # ';'

    def compile_let(self) -> None:
        """Compiles a let statement: letStatement: 'let' varName ('[' expression ']')? '=' expression ';'"""
        array_flag = False
        self.tokenizer.advance()  # 'let'
        name_ = self.tokenizer.identifier()
        self.tokenizer.advance()
        if self.tokenizer.symbol() == "[":
            array_flag = True
            self.array_handling(name_)
        self.tokenizer.advance()  # '='
        self.compile_expression()
        self.tokenizer.advance()  # ';'
        if array_flag:
            self.vm_writer.write_pop("TEMP", 0)
            self.vm_writer.write_pop("POINTER", 1)
            self.vm_writer.write_push("TEMP", 0)
            self.vm_writer.write_pop("THAT", 0)
        else:
            self.vm_writer.write_pop(CompilationEngine.VARS_MAP[self.symbol_table.kind_of(name_)],
                                     self.symbol_table.index_of(name_))

    def array_handling(self, name_: str) -> None:
        """Handles array handling: varName '[' expression ']'"""
        self.tokenizer.advance()  # '['
        self.compile_expression()
        self.tokenizer.advance()  # ']'
        if name_ in self.symbol_table.class_table or name_ in self.symbol_table.subroutine_table:
            if self.symbol_table.kind_of(name_) == "VAR":
                self.vm_writer.write_push("LOCAL", self.symbol_table.index_of(name_))
            elif self.symbol_table.kind_of(name_) == "ARG":
                self.vm_writer.write_push("ARG", self.symbol_table.index_of(name_))
            elif self.symbol_table.kind_of(name_) == "FIELD":
                self.vm_writer.write_push("THIS", self.symbol_table.index_of(name_))
            elif self.symbol_table.kind_of(name_) == "STATIC":
                self.vm_writer.write_push("STATIC", self.symbol_table.index_of(name_))
        self.vm_writer.write_arithmetic("+")

    def compile_while(self) -> None:
        """Compiles a while statement: 'while' '(' 'expression' ')' '{' statements '}'"""
        # 'while'
        this_while = self.symbol_table.while_id
        self.symbol_table.while_id += 1
        self.vm_writer.write_label(f"WHILE_EXP_{this_while}")
        self.tokenizer.advance()  # 'while'
        self.tokenizer.advance()  # '('
        self.compile_expression()
        self.vm_writer.write_arithmetic("NOT")
        self.vm_writer.write_if(f"WHILE_END_{this_while}")
        self.tokenizer.advance()  # ')'
        self.tokenizer.advance()  # '{'
        self.compile_statements()
        self.vm_writer.write_goto(f"WHILE_EXP_{this_while}")
        self.vm_writer.write_label(f"WHILE_END_{this_while}")
        self.tokenizer.advance()  # '}'

    def compile_return(self) -> None:
        """Compiles a return statement: 'return' expression? ';'"""
        return_void = True
        self.tokenizer.advance()  # 'return'
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ";":
            return_void = False
            self.compile_expression()
        if return_void:
            self.vm_writer.write_push("CONST", 0)
        self.vm_writer.write_return()
        self.tokenizer.advance()  # ';'

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else 
        clause: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?"""
        this_if = self.symbol_table.if_id
        self.symbol_table.if_id += 1
        self.tokenizer.advance()  # 'if'
        self.tokenizer.advance()  # '('
        self.compile_expression()
        self.tokenizer.advance()  # ')'
        self.vm_writer.write_if(f"IF_TRUE_{this_if}")
        self.vm_writer.write_goto(f"IF_FALSE_{this_if}")
        self.vm_writer.write_label(f"IF_TRUE_{this_if}")
        self.tokenizer.advance()  # '{'
        self.compile_statements()
        self.tokenizer.advance()  # '}'
        if self.tokenizer.keyword() == "ELSE":
            self.vm_writer.write_goto(f"IF_END_{this_if}")
            self.vm_writer.write_label(f"IF_FALSE_{this_if}")
            self.tokenizer.advance()  # 'else'
            self.tokenizer.advance()  # '{'
            self.compile_statements()
            self.tokenizer.advance()  # '}'
            self.vm_writer.write_label(f"IF_END_{this_if}")
        else:
            self.vm_writer.write_label(f"IF_FALSE_{this_if}")

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
        math_lib_ops = {"*": "Math.multiply", "/": "Math.divide"}
        all_ops = {"+", "-", "*", "/", "&", "|", "<", ">", "="}
        # Compile the first term
        self.compile_term()
        # Check and compile (op term)*
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() in all_ops:
            op_symbol = self.tokenizer.symbol()
            self.tokenizer.advance()  # the operator
            self.compile_term()  # Compile the next term
            if op_symbol in math_lib_ops:
                self.vm_writer.write_call(math_lib_ops[op_symbol], 2)
            else:
                self.vm_writer.write_arithmetic(op_symbol)

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
        unary_ops = {"-": "NEG", "~": "NOT", "^": "SHIFTLEFT", "#": "SHIFTRIGHT"}
        token_type = self.tokenizer.token_type()
        is_array = False
        if token_type == "INT_CONST":
            # Integer constant
            self.vm_writer.write_push("CONST", self.tokenizer.int_val())
            self.tokenizer.advance()
        elif token_type == "STRING_CONST":
            # String constant
            self.vm_writer.write_push("CONST", len(self.tokenizer.string_val()))
            self.vm_writer.write_call("String.new", 1)
            for char in self.tokenizer.string_val():
                self.vm_writer.write_push("CONST", ord(char))
                self.vm_writer.write_call("String.appendChar", 2)
            self.tokenizer.advance()
        elif token_type == "KEYWORD":
            # Keyword constant
            keyword = self.tokenizer.keyword()
            if keyword == "THIS":
                self.vm_writer.write_push("POINTER", 0)
            else:
                if keyword == "FALSE" or keyword == "NULL":
                    self.vm_writer.write_push("CONST", 0)
                if keyword == "TRUE":
                    self.vm_writer.write_push("CONST", 1)
                    self.vm_writer.write_arithmetic("NEG")
            self.tokenizer.advance()
        elif token_type == "SYMBOL":
            if self.tokenizer.symbol() == "(":
                # '(' expression ')'
                self.tokenizer.advance()  # '('
                self.compile_expression()
                self.tokenizer.advance()  # ')'
            elif self.tokenizer.symbol() in unary_ops:  # Unary operators
                unary_op = self.tokenizer.symbol()
                self.tokenizer.advance()
                self.compile_term()
                self.vm_writer.write_arithmetic(unary_ops[unary_op])
        elif token_type == "IDENTIFIER":
            vars_num = 0
            # Lookahead to distinguish between varName, array, and subroutineCall
            identifier = self.tokenizer.identifier()
            self.tokenizer.advance()
            if self.tokenizer.symbol() == "[":
                is_array = True
                self.array_handling(identifier)  # '[' expression ']'
            if self.tokenizer.symbol() == "(":
                vars_num += 1
                self.vm_writer.write_push("POINTER", 0)
                self.tokenizer.advance()  # '('
                vars_num += self.compile_expression_list()
                self.tokenizer.advance()  # ')'
                self.vm_writer.write_call(self.class_name + "." + identifier, vars_num)
            elif self.tokenizer.symbol() == ".":  # subroutineCall
                self.compile_subroutine_call(identifier)
            else:
                if is_array:
                    self.vm_writer.write_pop("POINTER", 1)
                    self.vm_writer.write_push("THAT", 0)
                elif identifier in self.symbol_table.class_table or identifier in self.symbol_table.subroutine_table:
                    identifier_kind_mapping = CompilationEngine.VARS_MAP[self.symbol_table.kind_of(identifier)]
                    self.vm_writer.write_push(identifier_kind_mapping, self.symbol_table.index_of(identifier))

    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        expression_num = 0
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ")":
            # There is at least one expression
            self.compile_expression()
            expression_num += 1
            while self.tokenizer.symbol() == ",":
                self.tokenizer.advance()  # ','
                self.compile_expression()
                expression_num += 1
        return expression_num

    def compile_subroutine_call(self, upper_identifier=None) -> None:
        """
        Compiles a subroutine call:
        - subroutineName '(' expressionList ')'
        - (className | varName) '.' subroutineName '(' expressionList ')'
        """
        vars_num = 0

        # Determine upper_identifier and subroutine name
        if upper_identifier is None:
            # If no explicit identifier is passed, read it from the tokenizer
            upper_identifier = self.tokenizer.identifier()
            self.tokenizer.advance()

            if self.tokenizer.symbol() == "(":
                # Direct subroutine call within the current class
                sub_identifier = upper_identifier
                upper_identifier = self.class_name
                self.vm_writer.write_push("POINTER", 0)  # Pass 'this' for method calls
                vars_num += 1
            elif self.tokenizer.symbol() == ".":
                # Object or class subroutine call
                self.tokenizer.advance()  # Advance past '.'
                sub_identifier = self.tokenizer.identifier()
                self.tokenizer.advance()
            else:
                raise ValueError("Unexpected token while parsing subroutine call.")
        else:
            # Case: explicit upper_identifier passed in
            self.tokenizer.advance()  # Advance past '.'
            sub_identifier = self.tokenizer.identifier()
            self.tokenizer.advance()

        # Determine if it's an instance method or static method
        if self.symbol_table.kind_of(upper_identifier):
            # It's an object instance
            kind_mapping = CompilationEngine.VARS_MAP[self.symbol_table.kind_of(upper_identifier)]
            self.vm_writer.write_push(
                kind_mapping,
                self.symbol_table.index_of(upper_identifier)
            )
            full_identifier = self.symbol_table.type_of(upper_identifier) + "." + sub_identifier
            vars_num += 1
        else:
            # It's a class
            full_identifier = upper_identifier + "." + sub_identifier

        # Compile expression list and emit the call
        self.tokenizer.advance()  # Advance past '('
        vars_num += self.compile_expression_list()
        self.tokenizer.advance()  # Advance past ')'
        self.vm_writer.write_call(full_identifier, vars_num)
