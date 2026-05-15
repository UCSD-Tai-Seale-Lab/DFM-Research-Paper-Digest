#!/usr/bin/env python3
"""
Author class
"""
from metapub import PubMedAuthor
from nameparser import HumanName

class Author(HumanName):
    ALIAS_PREVENTION_LIST: dict = {}

    def __init__(self, name: str | PubMedAuthor, **kwargs) -> None:
        self.__alias_prevention_dict: dict = {}
        self.first_initial_only: bool = None
        self.first_initial: str = None
        self.middle_initial_only: bool = None
        self.middle_initial: str = None
        self.must_show_as: str = None
        self.original: str = None
        self.pubmed_style: str = None
        self.slug: str = None

    def __first_names_or_initials_match(self, other_name: Author) -> bool: ...
    def __middle_names_match_where_present(self, other_name: Author) -> bool: ...
    def matches(
        self,
        other_name: (
            Author | PubMedAuthor | str | list[Author] | list[PubMedAuthor] | list[str]
        ),
    ) -> bool: ...
    @staticmethod
    def __remove_accents(input_str: str) -> str: ...
