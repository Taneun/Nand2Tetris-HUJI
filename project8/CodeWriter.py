"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""
    comp_counter = 0
    call_counter = 0
    TRUE = -1
    FALSE = 0
    COMMENT = "// "
    TEMP_START = 5
    VM_MAPPING = {
        "local": "LCL",
        "argument": "ARG",
        "this": "THIS",
        "that": "THAT",
        "temp": "R5",
        "pointer": "R3"
    }
    ARITHMETIC_DICT = {
        "add": "M=M+D",
        "sub": "M=M-D",
        "neg": "M=-M",
        "eq": "D;JEQ",
        "gt": "D;JGT",
        "lt": "D;JLT",
        "and": "M=D&M",
        "or": "M=D|M",
        "not": "M=!M",
        "shiftleft": "M=M<<",
        "shiftright": "M=M>>"
    }

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.output_file = output_stream
        self.curr_file_name = ""
        self.curr_function_name = ""

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self.curr_file_name = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        lines_to_write = ["@SP", "AM=M-1", "D=M"]
        # add as comment
        self.output_file.write(self.COMMENT + command + "\n")
        # add to file

        if command in ["neg", "not", "shiftleft", "shiftright"]:
            lines_to_write = ["@SP", "A=M-1", self.ARITHMETIC_DICT[command]]

        elif command in ["eq", "gt", "lt"]:
            self.compare_logic(command, lines_to_write)

        else:
            lines_to_write.extend(["A=A-1", self.ARITHMETIC_DICT[command]])

        for line in lines_to_write:
            self.output_file.write(line + "\n")

    def compare_logic(self, command, lines_to_write):
        CodeWriter.comp_counter += 1
        lines_to_write.extend([
            "@R13",  # Store y in R13
            "M=D",
            f"@Y_NEG_{command.upper()}_{CodeWriter.comp_counter}",
            "D;JLT",  # Jump if y < 0
            # Pop x (first operand) into D
            "@SP",
            "AM=M-1",
            "D=M",
            f"@Y_POS_X_NEG_{command.upper()}_{CodeWriter.comp_counter}",
            "D;JLT",  # Jump if x < 0
            "@R13",
            "D=D-M",
            f"@CHECK_{command.upper()}_{CodeWriter.comp_counter}",
            "0;JMP",  # Jump if x and y have different signs
            f"(Y_NEG_{command.upper()}_{CodeWriter.comp_counter})",  # Handle y < 0
            "@SP",
            "AM=M-1",
            "D=M",
            f"@Y_NEG_X_POS_{command.upper()}_{CodeWriter.comp_counter}",
            "D;JGT",  # Jump if x > 0
            "@R13",
            "D=D-M",
            f"@CHECK_{command.upper()}_{CodeWriter.comp_counter}",
            "0;JMP",  # Jump if x and y have different signs
            f"(Y_POS_X_NEG_{command.upper()}_{CodeWriter.comp_counter})",  # Handle x >= 0, y < 0
            "D=-1",
            f"@CHECK_{command.upper()}_{CodeWriter.comp_counter}",
            "0;JMP",
            f"(Y_NEG_X_POS_{command.upper()}_{CodeWriter.comp_counter})",  # Handle x < 0, y >= 0
            "D=1",
            f"@CHECK_{command.upper()}_{CodeWriter.comp_counter}",
            "0;JMP",
            f"(CHECK_{command.upper()}_{CodeWriter.comp_counter})",
            f"@TRUE_{command.upper()}_{CodeWriter.comp_counter}",
            self.ARITHMETIC_DICT[command],
            "D=0",
            f"@CONTINUE_{command.upper()}_{CodeWriter.comp_counter}",
            "0;JMP",
            f"(TRUE_{command.upper()}_{CodeWriter.comp_counter})",
            "D=-1",
            f"(CONTINUE_{command.upper()}_{CodeWriter.comp_counter})",
            "@SP",
            "A=M",
            "M=D",
            "@SP",
            "M=M+1"
        ])

    def write_push_constant(self, index: int) -> None:
        """Writes assembly code that affects the push constant command.

        Args:
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # The pseudo-code of "push constant i" is:
        # @i
        # D=A
        # @SP
        # A=M
        # M=D
        # @SP
        # M=M+1
        commands_list = ["D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
        self.output_file.write(f"@{index}\n")
        for command in commands_list:
            self.output_file.write(command + "\n")

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        pop_expression = ["@SP", "AM=M-1", "D=M"]
        push_expression = ["@SP", "A=M", "M=D", "@SP", "M=M+1"]
        lines_to_write = []
        # add as comment
        self.output_file.write(self.COMMENT + command + " " + segment + " " + str(index) + "\n")
        # add to file
        if command == "C_POP":
            self.pop_logic(index, lines_to_write, pop_expression, segment)

        if command == "C_PUSH":
            if segment == "constant":
                self.write_push_constant(index)
                return
            self.push_logic(index, lines_to_write, push_expression, segment)

        for line in lines_to_write:
            self.output_file.write(line + "\n")

    def push_logic(self, index, lines_to_write, push_expression, segment):
        if segment == "static":
            lines_to_write.append("@" + self.curr_file_name + "." + str(index))
            lines_to_write.append("D=M")
        elif segment == "temp":
            lines_to_write.append("@" + str(self.TEMP_START + index))
            lines_to_write.append("D=M")
        elif segment == "pointer":
            if index == 0:
                lines_to_write.append("@THIS")
            else:
                lines_to_write.append("@THAT")
            lines_to_write.append("D=M")
        else:
            lines_to_write.append("@" + self.VM_MAPPING[segment])
            lines_to_write.append("D=M")
            lines_to_write.append("@" + str(index))
            lines_to_write.append("A=D+A")
            lines_to_write.append("D=M")
        lines_to_write += push_expression

    def pop_logic(self, index, lines_to_write, pop_expression, segment):
        if segment in ["local", "argument", "this", "that"]:
            lines_to_write.append("@" + self.VM_MAPPING[segment])
            lines_to_write.append("D=M")
            lines_to_write.append("@" + str(index))
            lines_to_write.append("D=D+A")
            lines_to_write.append("@R13")
            lines_to_write.append("M=D")
            lines_to_write += pop_expression
            lines_to_write.append("@R13")
            lines_to_write.append("A=M")
        else:
            lines_to_write += pop_expression
            if segment == "pointer":
                if index == 0:
                    lines_to_write.append("@THIS")
                else:
                    lines_to_write.append("@THAT")
            elif segment == "temp":
                lines_to_write.append("@" + str(self.TEMP_START + index))
            elif segment == "static":
                lines_to_write.append("@" + self.curr_file_name + "." + str(index))
        lines_to_write.append("M=D")

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command.
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        self.output_file.write(f"{self.COMMENT} label {label}\n")
        self.output_file.write(f"({self.curr_function_name}${label})\n")

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        self.output_file.write(f"{self.COMMENT} goto {label}\n")
        self.output_file.write(f"@{self.curr_function_name}${label}\n")
        self.output_file.write("0;JMP\n")

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command.

        Args:
            label (str): the label to go to.
        """
        self.output_file.write(f"{self.COMMENT} if-goto {label}\n")
        commands_list = ["@SP", "AM=M-1", "D=M",
                         f"@{self.curr_function_name}${label}",
                         "D;JNE"]
        for command in commands_list:
            self.output_file.write(command + "\n")

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command.
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        self.output_file.write(f"{self.COMMENT} function {function_name} {n_vars} vars\n")
        self.curr_function_name = function_name
        # self.write_label(function_name)
        self.output_file.write(f"({function_name})\n")
        if n_vars > 0:
            self.output_file.write(f"{self.COMMENT} initializes {n_vars} variables to 0\n")
            self.output_file.write(f"@SP\nA=M\nM=0\n@SP\nM=M+1\n")
            for _ in range(n_vars-1):
                self.output_file.write(f"A=M\nM=0\n@SP\nM=M+1\n")

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command.
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        self.output_file.write(f"{self.COMMENT} call {function_name} {n_args} args\n")
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        return_address = f"{function_name}$ret.{CodeWriter.call_counter}"
        self.output_file.write(f"@{return_address}\n")
        self.output_file.write("D=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        for segment in ["LCL", "ARG", "THIS", "THAT"]:
            self.output_file.write(f"@{segment}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        # ARG = SP-5-n_args     // repositions ARG
        self.output_file.write(f"@SP\nD=M\n@5\nD=D-A\n@{n_args}\nD=D-A\n@ARG\nM=D\n")
        # LCL = SP              // repositions LCL
        self.output_file.write(f"@SP\nD=M\n@LCL\nM=D\n")
        # goto function_name    // transfers control to the callee
        self.output_file.write(f"@{function_name}\n0;JMP\n")
        # (return_address)      // injects the return address label into the code
        self.output_file.write(f"({return_address})\n")
        CodeWriter.call_counter += 1

    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        self.output_file.write(f"{self.COMMENT} return\n")
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        self.output_file.write(f"@LCL\nD=M\n@R13\nM=D\n")
        # return_address = *(frame-5)   // puts the return address in a temp var
        self.output_file.write(f"@5\nA=D-A\nD=M\n@R14\nM=D\n")
        # *ARG = pop()                  // repositions the return value for the caller
        self.output_file.write(f"@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n")
        # SP = ARG + 1                  // repositions SP for the caller
        self.output_file.write(f"@ARG\nD=M+1\n@SP\nM=D\n")
        # THAT = *(frame-1)             // restores THAT for the caller
        self.output_file.write(f"@R13\nAM=M-1\nD=M\n@THAT\nM=D\n")
        # THIS = *(frame-2)             // restores THIS for the caller
        self.output_file.write(f"@R13\nAM=M-1\nD=M\n@THIS\nM=D\n")
        # ARG = *(frame-3)              // restores ARG for the caller
        self.output_file.write(f"@R13\nAM=M-1\nD=M\n@ARG\nM=D\n")
        # LCL = *(frame-4)              // restores LCL for the caller
        self.output_file.write(f"@R13\nAM=M-1\nD=M\n@LCL\nM=D\n")
        # goto return_address           // go to the return address
        self.output_file.write(f"@R14\nA=M\n0;JMP\n")

    def write_init(self) -> None:
        """Writes assembly code that initializes the VM."""
        self.output_file.write(f"{self.COMMENT} init\n")
        # The pseudo-code of "init" is:
        # SP = 256
        self.output_file.write(f"@256\nD=A\n@SP\nM=D\n")
        # call Sys.init
        self.write_call("Sys.init", 0)
