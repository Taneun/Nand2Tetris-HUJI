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
        input_lines = input_file.read().splitlines()
        self.only_commands = [line.split("//")[0].replace(" ", "") for line in input_lines if
                              not (line.strip() == "" or line.startswith("//"))]
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
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        self.curr_line_index += 1
        if self.has_more_commands():
            self.curr_line = self.only_commands[self.curr_line_index]

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if self.curr_line.startswith("@"):
            return "A_COMMAND"
        elif self.curr_line.startswith("("):
            return "L_COMMAND"
        return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        if self.command_type() == "A_COMMAND":
            return self.curr_line[1:]
        elif self.command_type() == "L_COMMAND":
            return self.curr_line[1:-1]

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if self.command_type() == "C_COMMAND":
            if "=" in self.curr_line:
                return self.curr_line.split("=")[0]
            return "null"

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if self.command_type() == "C_COMMAND":
            if "=" in self.curr_line:
                return self.curr_line.split("=")[1].split(";")[0]
            else:
                comp_ = self.curr_line.split(";")[0]
                return comp_

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if self.command_type() == "C_COMMAND":
            if ";" in self.curr_line:
                return self.curr_line.split(";")[1]
            return "null"

    def reset(self) -> None:
        """Resets the parser to the beginning of the file."""
        self.curr_line_index = 0
        # self.memory_address = 0
        self.curr_line = self.only_commands[0]
