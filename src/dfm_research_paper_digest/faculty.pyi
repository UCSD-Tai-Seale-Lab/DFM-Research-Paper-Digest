from __future__ import annotations

import logging
from pathlib import Path

from metapub import PubMedAuthor

from src.dfm_research_paper_digest.author import Author  # pylint: disable=import-error

class Faculty:
    # Can create from existing hard-coded list, a filename or a Path object.
    def __init__(self, faculty_list: list[str] | str | Path, log: logging.Logger):
        self.__list: list[Author] = None
        self.__log: logging.Logger = None
        self.authors: list[Author] = None
        self.names: list[str] = None
        self.num: int = None
        self.original_names: list[str] = None

    def is_faculty(self, author: Author | PubMedAuthor | str) -> bool: ...
    def __is_url(self, name: str | Path) -> bool: ...
    def __names(self) -> list[str]: ...
    def __original_names(self) -> list[str]: ...
    def __read_faculty_list_file(self, file: str | Path) -> list[str]: ...
    def __scrape_webpage(self, site_address: str) -> list[str]: ...
