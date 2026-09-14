"""
Author class
"""

from typing import ClassVar

from metapub import PubMedAuthor
from nameparser import HumanName

class Author(HumanName):
    ALIAS_PREVENTION_LIST: ClassVar[dict] = None
    __alias_prevention_dict: dict = None
    first_initial_only: bool = None
    first_initial: str = None
    middle_initial_only: bool = None
    middle_initial: str = None
    must_show_as: str = None
    _original: str = None
    pubmed_style: str = None
    slug: str = None

    def __init__(self, name: str | PubMedAuthor, **kwargs) -> None: ...
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
