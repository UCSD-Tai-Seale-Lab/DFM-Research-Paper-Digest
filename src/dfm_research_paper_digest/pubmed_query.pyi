import logging
from datetime import datetime

from metapub import PubMedArticle, PubMedAuthor, PubMedFetcher

def display_publications(
    publications: list[PubMedArticle], log: logging.Logger
) -> None: ...
def export_to_csv(
    publications: list[PubMedArticle], filename: str, log: logging.Logger
) -> None: ...

class PubMedQuery:
    def __init__(self, email: str = None, log: logging.Logger = None):
        self.__fetch: PubMedFetcher = None
        self.__log: logging.Logger = None

    def display_publications(
        publications: list[PubMedArticle], log: logging.Logger
    ): ...
    def __fetch_publication_details(
        self, pmids: list[str], author_name: str
    ) -> list[PubMedArticle]: ...
    @staticmethod
    def is_ucsd_affiliated(var: list[str] | PubMedAuthor) -> bool: ...
    def query_by_author(
        self, author_name: str, year: int = datetime.now().year
    ) -> list[PubMedArticle]: ...
    def __search_author_publications(
        self, author_name: str, year: int = datetime.now().year
    ) -> list[str]: ...
