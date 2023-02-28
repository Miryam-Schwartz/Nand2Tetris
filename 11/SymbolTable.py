"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        self._class_scope = {}
        self._subroutine_scope = {}
        self._static_count = 0
        self._field_count = 0
        self._arg_count = 0
        self._var_count = 0

    def start_subroutine(self) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        self._subroutine_scope.clear()
        self._arg_count = 0
        self._var_count = 0

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
        if kind == "STATIC":
            self._class_scope[name] = (type, kind, self._static_count)
            self._static_count += 1
        elif kind == "FIELD":
            self._class_scope[name] = (type, kind, self._field_count)
            self._field_count += 1
        elif kind == "ARG":
            self._subroutine_scope[name] = (type, kind, self._arg_count)
            self._arg_count += 1
        elif kind == "VAR":
            self._subroutine_scope[name] = (type, kind, self._var_count)
            self._var_count += 1

    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        if kind == "STATIC":
            return self._static_count
        elif kind == "FIELD":
            return self._field_count
        elif kind == "ARG":
            return self._arg_count
        elif kind == "VAR":
            return self._var_count

    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        if name in self._subroutine_scope:
            return self._subroutine_scope[name][1]
        if name in self._class_scope:
            return self._class_scope[name][1]

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        if name in self._subroutine_scope:
            return self._subroutine_scope[name][0]
        if name in self._class_scope:
            return self._class_scope[name][0]

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        if name in self._subroutine_scope:
            return self._subroutine_scope[name][2]
        if name in self._class_scope:
            return self._class_scope[name][2]
