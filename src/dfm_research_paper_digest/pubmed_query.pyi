import logging
from datetime import datetime

from metapub import PubMedArticle, PubMedAuthor, PubMedFetcher

import src.dfm_research_paper_digest

def display_publications(
    publications: list[PubMedArticle], log: logging.Logger
) -> None: ...
def export_to_csv(
    publications: list[PubMedArticle], filename: str, log: logging.Logger
) -> None: ...
def main(argv=None) -> None: ...

class PubMedQuery:
    UCSD_AFFILIATIONS: str = ""
    def __init__(
        self,
        faculty: src.dfm_research_paper_digest.Faculty,
        email: str = None,
        log: logging.Logger = None,
    ):
        self.__faculty: src.dfm_research_paper_digest.Faculty = None
        self.__fetcher: PubMedFetcher = None
        self.__log: logging.Logger = None
        self.__using_streamlit: bool = None

    def __fetch_publication_details(
        self, pmids: list[str], author_name: str
    ) -> list[PubMedArticle]: ...
    @staticmethod
    def is_ucsd_affiliated(var: list[str] | PubMedAuthor | str) -> bool: ...
    def query_by_author(
        self, author_name: str, year: int = datetime.now().year
    ) -> list[PubMedArticle]: ...
    def __search_author_publications(
        self, author_name: str, year: int = datetime.now().year
    ) -> list[str]: ...
