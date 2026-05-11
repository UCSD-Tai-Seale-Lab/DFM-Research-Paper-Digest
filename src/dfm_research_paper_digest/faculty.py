#!/usr/bin/env python3
"""
Faculty class
"""
from __future__ import annotations

import copy
import logging
from pathlib import Path
from urllib.parse import ParseResult, urlparse

import bs4
import requests
from bs4 import BeautifulSoup
from metapub import PubMedAuthor

from dfm_research_paper_digest import Author  # pylint: disable=import-error


# pylint: disable=too-few-public-methods
class Faculty:
    """
    Holds a list of Author objects & allows modules to ask whether
    a particular Author is in this list, allowing for middle name/initial ambiguity.

    Attributes:
    ----------
    authors: list[Author]
    names: list[str]
    num: int
    original_names: list[str]

    Methods
    -------
    is_faculty(): bool
    """

    # Can create from existing hard-coded list, a filename or a Path object.
    def __init__(self, faculty_list: list[str] | str | Path, log: logging.Logger):
        self.__list: list[Author]
        self.__log: logging.Logger = log

        if isinstance(faculty_list, list):
            self.__list = [Author(f) for f in faculty_list]
        elif isinstance(faculty_list, (str, Path)):
            lines: list[str] = []

            if self.__is_url(faculty_list):
                lines = self.__scrape_webpage(faculty_list)
            else:
                lines = self.__read_faculty_list_file(faculty_list)

            if lines:
                self.__list = [Author(f) for f in lines]
            else:
                self.__log.exception(f"Unable to find/read file {faculty_list}.")
                raise FileNotFoundError(f"Unable to open file {faculty_list}.")
        else:
            self.__log.exception(
                f"Expected 'faculty_list' to be a list, str or Path, not {type(faculty_list)}."
            )
            raise TypeError(
                f"Expected 'faculty_list' to be a list, str or Path, not {type(faculty_list)}."
            )

        self.authors: list[Author] = copy.deepcopy(self.__list)
        self.names: list[str] = self.__names()
        self.num: int = len(self.__list)
        self.original_names: list[str] = self.__original_names()

    def is_faculty(self, var: Author | PubMedAuthor | str) -> bool:
        """
        Tests an Author to see if it matches any of our faculty members.

        Parameters
        ----------
        var: Author or PubMedAuthor or str

        Returns
        -------
        match: bool
        """
        author: Author

        if isinstance(var, str):
            author = Author(var)
        elif isinstance(var, Author):
            author = var
        elif isinstance(var, PubMedAuthor):
            author = Author(f"{var.fore_name} {var.last_name}")
        else:
            self.__log.exception(
                "Type Error: Expected 'var' to be Author object or str."
            )
            raise TypeError("Expected 'var' to be Author object or str.")

        for faculty_member in self.__list:
            if author.matches(faculty_member):
                return True

        return False

    def __is_url(self, name: str | Path) -> bool:
        """
            Parses string to see if it could be a URL address

        Parameters
        ----------
        name: str | Path

        Returns
        -------
        bool
        """
        if isinstance(name, Path):
            return False

        if isinstance(name, str):
            parsed: ParseResult = urlparse(name)

            # A URL typically has a scheme (http/https) and a domain (netloc)
            return all([parsed.scheme, parsed.netloc])
        else:
            self.__log.exception(
                f"Expected 'name' to be str or Path, not {type(name)}."
            )
            raise TypeError(f"Expected 'name' to be str or Path, not {type(name)}.")

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
        faculty_lines: list[str]

        if not isinstance(file, str) and not isinstance(file, Path):
            self.__log.exception(
                f"Expected 'file' to be str or Path, not {type(file)}."
            )
            raise TypeError(f"Expected 'file' to be str or Path, not {type(file)}.")

        try:
            with open(file, "r", encoding="utf-8") as f:
                faculty_lines = [line.strip() for line in f if line.strip()]

            self.__log.info(f"Loaded {len(faculty_lines)} faculty members.")

            return faculty_lines

        except FileNotFoundError:
            self.__log.error(f"Warning: Faculty list file not found: {file}.")
        except Exception as e:
            self.__log.exception(f"Error loading faculty list: {e}.")

        return []

    def __scrape_webpage(self, site_address: str) -> list[str]:
        """
            Scrape faculty webpage and extract a list of faculty members.

        Parameters
        ----------
        site_address

        Returns
        -------
        names: list[str]
        """
        if not isinstance(site_address, str):
            self.__log.exception(
                f"Expected 'site_address' to be str, not {type(site_address)}."
            )
            raise TypeError(
                f"Expected 'site_address' to be str, not {type(site_address)}."
            )

        response: requests.Response = requests.get(site_address)
        soup: bs4.BeautifulSoup = BeautifulSoup(response.text, "html.parser")
        names: list[str] = []

        tags: bs4.ResultSet = soup.find_all("td", class_="sorting_1")

        for tag in tags:
            names.append(tag.get_text().strip())

        # The faculty webpage lists Prof. Ming Tai-Seale as just "Tai-Seale, PhD, MPH"
        names_repaired: list[str] = [
            "Tai-Seale, Ming PhD, MPH" if "Tai-Seale" in item else item
            for item in names
        ]
        names_repaired.sort()
        return names_repaired
