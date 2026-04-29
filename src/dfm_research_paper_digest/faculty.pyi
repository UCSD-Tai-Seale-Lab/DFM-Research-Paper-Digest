from __future__ import annotations

import logging
from pathlib import Path

from src.dfm_research_paper_digest.author import Author

class Faculty:
    # Can create from existing hard-coded list, a filename or a Path object.
    def __init__(self, faculty_list: list[str] | str | Path, log: logging.Logger):
        self.__list: list[Author] = None
        self.__log: logging.Logger = None
        self.authors: list[Author] = None
        self.names: list[str] = None
        self.num: int = None
        self.original_names: list[str] = None

    def __read_faculty_list_file(self, file: str | Path) -> list[str]: ...
    def is_faculty(self, author: Author | str) -> bool: ...
    def __names(self) -> list[str]: ...
    def __original_names(self) -> list[str]: ...
