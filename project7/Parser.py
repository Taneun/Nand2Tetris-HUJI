"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    # Parser
    
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.

    ## VM Language Specification

    A .vm file is a stream of characters. If the file represents a
    valid program, it can be translated into a stream of valid assembly 
    commands. VM commands may be separated by an arbitrary number of whitespace
    characters and comments, which are ignored. Comments begin with "//" and
    last until the line’s end.
    The different parts of each VM command may also be separated by an arbitrary
    number of non-newline whitespace characters.

    - Arithmetic commands:
      - add, sub, and, or, eq, gt, lt
      - neg, not, shiftleft, shiftright
    - Memory segment manipulation:
      - push <segment> <number>
      - pop <segment that is not constant> <number>
      - <segment> can be any of: argument, local, static, constant, this, that, 
                                 pointer, temp
    - Branching (only relevant for project 8):
      - label <label-name>
      - if-goto <label-name>
      - goto <label-name>
      - <label-name> can be any combination of non-whitespace characters.
    - Functions (only relevant for project 8):
      - call <function-name> <n-args>
      - function <function-name> <n-vars>
      - return
    """
    COMMANDS = {
        # all arithmetic commands are of type C_ARITHMETIC
        "add": "C_ARITHMETIC",
        "sub": "C_ARITHMETIC",
        "neg": "C_ARITHMETIC",
        "eq": "C_ARITHMETIC",
        "gt": "C_ARITHMETIC",
        "lt": "C_ARITHMETIC",
        "and": "C_ARITHMETIC",
        "or": "C_ARITHMETIC",
        "not": "C_ARITHMETIC",
        "shiftleft": "C_ARITHMETIC",
        "shiftright": "C_ARITHMETIC",
        "pop": "C_POP",
        "push": "C_PUSH",
        "label": "C_LABEL",
        "goto": "C_GOTO",
        "if-goto": "C_IF",
        "function": "C_FUNCTION",
        "call": "C_CALL",
        "return":  "C_RETURN"
    }

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        input_lines = input_file.read().splitlines()
        self.only_commands = [line.split("//")[0].split() for line in input_lines if
                              not (line == "" or line.startswith("//"))]
        self.code_length = len(self.only_commands)
        self.curr_line_index = 0
        self.curr_line = self.only_commands[0]

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.curr_line_index < self.code_length

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        self.curr_line_index += 1
        if self.has_more_commands():
            self.curr_line = self.only_commands[self.curr_line_index]

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        return Parser.COMMANDS[self.curr_line[0]]

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        # todo: check on return command here?
        if self.command_type() == "C_ARITHMETIC":
            return self.curr_line[0]
        return self.curr_line[1]

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        # todo: check on command here?
        return int(self.curr_line[2])
