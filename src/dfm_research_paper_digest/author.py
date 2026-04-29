#!/usr/bin/env python3
"""
Author class
"""
from __future__ import annotations

from typing import Self

from nameparser import HumanName


class Author(HumanName):
    """
    Allows custom matching of names. Inherits from nameparser.HumanName

    Attributes:
    ----------
    first: str                  author's given name
    last: str                   author's family name
    middle: str                 author's middle name
    middle_initial:             author's middle initial
    middle_initial_only: bool   True if author's name has a middle initial but not a full name
    original: str               name used to instantiate the object
    pubmed_style: str           Last, First format
    slug: str                   name with spaces replaced with underscores

    Methods
    -------
    matches()                   Tests if two authors match, allowing for middle name/initial ambiguity
    """

    def __init__(self, name: str, **kwargs):
        """
        Instantiates an Author object from a string name.
        """
        super().__init__(name, **kwargs)

        self.middle_initial_only: bool = False
        self.middle_initial: str = ""
        self.original: str = name

        # Add extra properties
        if self.middle:
            self.middle_initial_only = len(self.middle.rstrip(".")) == 1
            self.middle_initial = self.middle[0]

        self.pubmed_style: str = self.last + ", " + self.first
        self.slug: str = name.replace(" ", "_").replace(",", "").replace('"', "")

    def __middle_names_match_where_present(self, other_name: Self) -> bool:
        """
        Returns True if:
            * middle_name_A is empty
            * middle_name_B is empty
            * middle_name_A == middle_name_B
            * middle_name_A is only one char and matches first char of middle_name_B
            * middle_name_B is only one char and matches first char of middle_name_A

        Examples:
                middle_name_A       middle_name_B       result
            *       ''                  'Juan'            True
            *       'Juan'              ''                True
            *       'Juan'              'Juan'            True
            *       'J'                 'Juan'            True
            *       'Juan'              'J'               True
            *       'J'                 'J'               True
            *       ''                  ''                True
            *       'X'                 'J'              False
            *       'X'                 'Juan'           False
            *       'Juan'              'Z'              False

        Parameters
        ----------
        middle_name_A: str
        middle_name_B: str

        Returns
        -------
        match: bool
        """
        if self.middle:
            if other_name.middle:
                if self.middle == other_name.middle:
                    return True
                elif (
                    self.middle_initial_only
                    and self.middle_initial == other_name.middle_initial
                ):
                    return True
                elif (
                    other_name.middle_initial_only
                    and self.middle_initial == other_name.middle_initial
                ):
                    return True
            else:
                return True
        else:
            return True

        return False

    def matches(self, other_name: Self | str | list[Self] | list[str]) -> bool:
        """
        Tests matching of first, last and (if present) middle names.
        If other_name is a list of Authors, returns True if ANY match self.

        Parameters
        ----------
        other_name: Author or list[Author] or list[str]

        Returns
        -------
        match: bool
        """
        # Is it a LIST (of either str or Author)
        if isinstance(other_name, list):
            for name in other_name:
                if self.matches(name):
                    return True

            return False

        # Is it a STR?
        if isinstance(other_name, str):
            return self.matches(Author(other_name))

        # It's an Author.
        return (
            self.first == other_name.first
            and self.last == other_name.last
            and self.__middle_names_match_where_present(other_name)
        )
