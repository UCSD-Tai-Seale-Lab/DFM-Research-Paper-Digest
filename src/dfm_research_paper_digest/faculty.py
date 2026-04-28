#!/usr/bin/env python3
"""
Faculty class
"""
from __future__ import annotations
import copy
import logging
from pathlib import Path

from src.dfm_research_paper_digest.author import Author


class Faculty:
    """
    Holds a list of Author objects & allows modules to ask whether
    a particular Author is in this list, allowing for middle name/initial ambiguity.

    Attributes:
    ----------
    num: int

    Methods
    -------
    is_faculty(): bool
    names(): list[str]
    """

    # Can create from existing hard-coded list, a filename or a Path object.
    def __init__(self, faculty_list: list[str] | str | Path, log: logging.Logger):
        self.__list: list[Author]
        self.__log: logging.Logger = log

        if isinstance(faculty_list, list):
            self.__list = [Author(f) for f in faculty_list]
        elif isinstance(faculty_list, (str, Path)):
            lines: list[str] = self.__read_faculty_list_file(faculty_list)
            self.__list = [Author(f) for f in lines]

        self.authors: list[Author] = copy.deepcopy(self.__list)
        self.names: list[str] = self.__names()
        self.num: int = len(self.__list)
        self.original_names: list[str] = self.__original_names()

    def is_faculty(self, author: Author) -> bool:
        """
        Tests an Author to see if it matches any of our faculty members.

        Parameters
        ----------
        author: Author

        Returns
        -------
        match: bool
        """
        for faculty_member in self.__list:
            if author.matches(faculty_member):
                return True

        return False

    def __names(self) -> list[str]:
        """
        Generates a list of Author names in last, first format.

        Returns
        -------
        authors: list[str]
        """
        authors: list[str] = []

        for member in self.__list:
            authors.append(member.pubmed_style)

        return authors

    def __original_names(self) -> list[str]:
        """
        Generates a list of Author names in original format.

        Returns
        -------
        authors: list[str]
        """
        authors: list[str] = []

        for member in self.__list:
            authors.append(member.original)

        return authors

    def __read_faculty_list_file(self, file: str | Path) -> list[str]:
        """
        Reads faculty list file into list of strings.

        Parameters
        ----------
        file: str or Path

        Returns
        -------
        lines: list[str]
        """
        try:
            faculty_lines: list[str]

            with open(file, "r") as f:
                faculty_lines = [line.strip() for line in f if line.strip()]

            self.__log.info(
                f"Loaded {len(faculty_lines)} faculty members for highlighting."
            )

            return faculty_lines

        except FileNotFoundError:
            self.__log.error(f"Warning: Faculty list file not found: {file}.")
        except Exception as e:
            self.__log.exception(f"Error loading faculty list: {e}.")
