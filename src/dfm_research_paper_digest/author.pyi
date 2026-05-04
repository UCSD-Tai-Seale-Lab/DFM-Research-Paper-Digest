#!/usr/bin/env python3
"""
Author class
"""
from nameparser import HumanName

class Author(HumanName):
    def __init__(self, name: str, **kwargs) -> None:
        self.affiliation: str = None
        self.middle_initial_only: bool = None
        self.middle_initial: str = None
        self.original: str = None
        self.pubmed_style: str = None
        self.slug: str = None

    def add_affiliation(self, affiliation: str) -> None: ...
    def is_ucsd(self) -> bool: ...
    def __middle_names_match_where_present(self, other_name: Author) -> bool: ...
    def matches(self, other_name: Author | str | list[Author] | list[str]) -> bool: ...
