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


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    rom_address = 16
    to_reduce = 0
    parser = Parser(input_file)
    symbol_table = SymbolTable()
    while parser.has_more_commands():
        if parser.command_type() == "L_COMMAND" and not symbol_table.contains(parser.symbol()):
            symbol_table.add_entry(parser.symbol(), parser.curr_line_index - to_reduce) #todo here
            to_reduce += 1
        parser.advance()
    parser.reset()
    while parser.has_more_commands():
        new_line = ""
        command_type = parser.command_type()
        if command_type == "A_COMMAND":
            symbol = parser.symbol()
            if symbol.isdigit():
                address = int(symbol)
            else:
                if not symbol_table.contains(symbol):
                    symbol_table.add_entry(symbol, rom_address)
                    rom_address += 1
                address = symbol_table.get_address(symbol)

            new_line = format(address, "016b")
        elif command_type == "C_COMMAND":
            dest_ = Code.dest(parser.dest())
            comp_ = Code.comp(parser.comp())
            jump_ = Code.jump(parser.jump())
            ones_to_add = "1" * (16 - len(dest_ + comp_ + jump_))
            new_line = ones_to_add + comp_ + dest_ + jump_

        parser.advance()
        if new_line != "":
            output_file.write(new_line + "\n")


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
