#!/usr/bin/env python3
"""
Author class
"""
from __future__ import annotations

import unicodedata
from typing import Self

from metapub import PubMedAuthor
from nameparser import HumanName


class Author(HumanName):
    """
    Allows custom matching of names. Inherits from nameparser.HumanName

    Attributes:
    ----------
    first: str                  author's given name
    first_initial:              author's first initial
    first_initial_only: bool    True if author's name has a first initial but not a full name
    last: str                   author's family name
    middle: str                 author's middle name
    middle_initial:             author's middle initial
    middle_initial_only: bool   True if author's name has a middle initial but not a full name
    original: str               name used to instantiate the object
    pubmed_style: str           Last Name, First Initial format
    slug: str                   Name formatted as filename
    Methods
    -------
    matches()                   Tests if two authors match,
                                 allowing for middle name/initial ambiguity
    """

    def __init__(self, name: str | PubMedAuthor, **kwargs):
        """
        Instantiates an Author object from a string name or PubMedAuthor object.
        """
        name_str: str = ""

        if isinstance(name, PubMedAuthor):
            name_str = name.fore_name + " " + name.last_name
        elif isinstance(name, str):
            name_str = name
        else:
            raise TypeError(
                f"Expected 'name' to be str or PubMedAuthor, not {type(name)}."
            )

        # Remove any accents for easier matching.
        super().__init__(self.__remove_accents(name_str), **kwargs)

        self.first_initial_only: bool = False
        self.first_initial: str = ""
        self.middle_initial_only: bool = False
        self.middle_initial: str = ""
        self.original: str = name_str

        # Add extra properties
        if self.first:
            self.first_initial_only = len(self.first.rstrip(".")) == 1
            self.first_initial = self.first[0]

        if self.middle:
            self.middle_initial_only = len(self.middle.rstrip(".")) == 1
            self.middle_initial = self.middle[0]

        self.pubmed_style: str = self.last + ", " + self.first_initial
        self.slug: str = name_str.replace(" ", "_").replace(",", "").replace('"', "")

    def __first_names_or_initials_match(self, other_name: Self) -> bool:
        """
        Returns True if:
            * first_name_A == first_name_B
            * first_name_A is only one char and matches first char of first_name_B
            * first_name_B is only one char and matches first char of first_name_A

        Examples:
                first_name_A       first_name_B       result
            *       'Juan'              'Juan'            True
            *       'J'                 'Juan'            True
            *       'Juan'              'J'               True
            *       'J'                 'J'               True
            *       ''                  ''                True
            *       'X'                 'J'              False
            *       'X'                 'Juan'           False
            *       'Juan'              'X'              False

        Parameters
        ----------
        first_name_A: str
        first_name_B: str

        Returns
        -------
        match: bool
        """
        if self.first == other_name.first:
            return True

        if self.first_initial_only and self.first_initial == other_name.first_initial:
            return True

        if (
            other_name.first_initial_only
            and self.first_initial == other_name.first_initial
        ):
            return True

        return False

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
            *       'Juan'              'X'              False

        Parameters
        ----------
        middle_name_A: str
        middle_name_B: str

        Returns
        -------
        match: bool
        """
        if not self.middle:
            return True

        if not other_name.middle:
            return True

        if self.middle == other_name.middle:
            return True

        if (
            self.middle_initial_only
            and self.middle_initial == other_name.middle_initial
        ):
            return True

        if (
            other_name.middle_initial_only
            and self.middle_initial == other_name.middle_initial
        ):
            return True

        return False

    def matches(
        self,
        other_name: (
            Self | PubMedAuthor | str | list[Self] | list[PubMedAuthor] | list[str]
        ),
    ) -> bool:
        """
        Tests matching of first, last and (if present) middle names.
        If other_name is a list of Authors, returns True if ANY match self.

        Parameters
        ----------
        other_name: Author, PubMedAuthor, str or list of those

        Returns
        -------
        match: bool
        """
        # Is it a LIST (of either str or Author or PubMedAuthor)
        if isinstance(other_name, list):
            for name in other_name:
                if self.matches(name):
                    return True

            return False

        # Is it a str?
        if isinstance(other_name, str):
            return self.matches(Author(self.__remove_accents(other_name)))

        if isinstance(other_name, PubMedAuthor):
            # Create a new Author object & use that.
            try:
                other_author: Author = Author(
                    other_name.fore_name + " " + other_name.last_name
                )
                return self.matches(other_author)
            except TypeError:
                # If the PubMed "Author" can't be parsed,
                # it's probably corporate and won't match any of our faculty names.
                return False

        # It's an Author.
        return (
            self.__first_names_or_initials_match(other_name)
            and self.last == other_name.last
            and self.__middle_names_match_where_present(other_name)
        )

    # Source - https://stackoverflow.com/a/517974
    # Posted by MiniQuark, modified by community. See post 'Timeline' for change history
    # Retrieved 2026-05-08, License - CC BY-SA 3.0
    @staticmethod
    def __remove_accents(input_str: str) -> str:
        nfkd_form = unicodedata.normalize("NFKD", input_str)
        name_no_accents: str = "".join(
            [c for c in nfkd_form if not unicodedata.combining(c)]
        )
        return name_no_accents
