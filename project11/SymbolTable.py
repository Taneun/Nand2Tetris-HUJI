"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from collections import namedtuple


class SymbolTable:
    SUBROUTINE_SCOPE = ["ARG", "VAR"]
    CLASS_SCOPE = ["STATIC", "FIELD"]
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        self.Symbol = namedtuple('Symbol', ['type', 'kind', 'index'])
        self.counter_dict = {"class": {"STATIC": 0,
                                       "FIELD": 0},
                             "subroutine": {"ARG": 0,
                                            "VAR": 0}}
        self.class_table = {}
        self.subroutine_table = None
        self.while_id = 0
        self.if_id = 0

    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        self.subroutine_table = {}
        self.counter_dict["subroutine"]["ARG"] = 0
        self.counter_dict["subroutine"]["VAR"] = 0

    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        s = self.Symbol(type, kind, self.var_count(kind))
        if kind in SymbolTable.CLASS_SCOPE:
            self.class_table[name] = s
            self.counter_dict["class"][kind] += 1
        else:
            self.subroutine_table[name] = s
            self.counter_dict["subroutine"][kind] += 1

    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        if kind in SymbolTable.CLASS_SCOPE:
            return self.counter_dict["class"][kind]
        else:
            return self.counter_dict["subroutine"][kind]

    def kind_of(self, name: str) -> str | None:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        if name in self.subroutine_table:
            return self.subroutine_table[name].kind
        elif name in self.class_table:
            return self.class_table[name].kind
        return None

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        if name in self.subroutine_table:
            return self.subroutine_table[name].type
        elif name in self.class_table:
            return self.class_table[name].type

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        if name in self.subroutine_table:
            return self.subroutine_table[name].index
        elif name in self.class_table:
            return self.class_table[name].index

